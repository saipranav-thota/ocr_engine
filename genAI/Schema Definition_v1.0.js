// MongoDB Schema – Clean, Modular, and Scalable
// Based on architectural decisions made on pacing, reinforcement, chat-content separation, and on-demand item generation

// --------------------
// 1. User Collection
// --------------------
const User = {
  _id: ObjectId,
  name: String,
  email: String,
  preferences: {
    pacing: "fast" | "balanced" | "relaxed", // used when generating review schedules
    preferredStudyTime: "morning" | "evening" | "flexible",
    notifications: {
      enabled: Boolean,
      frequency: "daily" | "weekly",
      time: String
    }
  },
  status: "active" | "archived" | "deleted", // soft deletion or lifecycle state
  createdAt: Date,
  updatedAt: Date
};

// --------------------
// 2. ChatSession Collection
// --------------------
const ChatSession = {
  _id: ObjectId,
  userId: ObjectId,
  messages: [
    {
      role: "user" | "assistant",
      content: String,
      timestamp: Date
    }
  ],
  summary: String, // optional auto-generated summary of the session
  reinforcementItemIds: [ObjectId], // linked reinforcement content (optional, if pre-generated)
  status: "active" | "archived" | "deleted",
  createdAt: Date,
  updatedAt: Date
};

// --------------------
// 3. Content Collection
// Stores the uploaded content
// For non-chat uploads, Content exists on its own
// For chat-context uploads, Content has chatSessionId
// --------------------
const Content = {
  _id: ObjectId,
  userId: ObjectId,
  chatSessionId: ObjectId, // optional – only if uploaded during a chat
  sourceType: "voice" | "document" | "image",
  fileInfo: {
    filename: String,
    format: String,
    size: Number,
    location: String, // blob URI (e.g., Azure Blob Storage)
    transcription: String // applicable for audio/image with OCR/STT
  },
  extractedText: String,
  reinforcementItemIds: [ObjectId], // optional, for cached/generated items
  autoTagged: Boolean,
  reviewedByOrchestrator: Boolean,
  confidenceScore: Number, // if AI-classified content
  status: "active" | "archived" | "deleted",
  createdAt: Date,
  updatedAt: Date
};

// --------------------
// 4. ReviewSchedule
// Created per content or chatSession
// May dynamically trigger multiple ReinforcementItems
// --------------------
const ReviewSchedule = {
  _id: ObjectId,
  userId: ObjectId,
  contentId: ObjectId, // optional – for standalone resources
  chatSessionId: ObjectId, // optional – for chat-based recall
  scheduledDate: Date, // one MongoDB document per revision instance
  status: "scheduled" | "completed" | "partial" | "missed",
  completedAt: Date,
  feedback: {
    selfReflection: "got_it" | "needs_review" | null, // shown only at topic-level completion
    accuracyScore: Number // quiz or flashcard performance during review
  },
  reinforcementType: "quiz" | "flashcard" | "review" | "teachMeBack",
  createdAt: Date,
  updatedAt: Date
};

// --------------------
// 5. ReinforcementItem
// Created dynamically during ReviewSchedule or On-demand
// --------------------
const ReinforcementItem = {
  _id: ObjectId,
  type: "flashcard" | "MCQ" | "quiz" | "teachMeBack",
  sourceType: "content" | "chat",
  sourceId: ObjectId, // contentId or chatSessionId
  reviewScheduleId: ObjectId, // optional – populated if user used the ReinforcementItem as per the ReviewSchedule
  question: String,
  options: [String], // applicable for MCQ
  correctAnswer: String,
  difficulty: "easy" | "medium" | "hard",
  createdAt: Date
};

// --------------------
// 6. IndexSnapshot (for scoring over time)
// --------------------
const IndexSnapshot = {
  _id: ObjectId,
  userId: ObjectId,
  timestamp: Date,
  score: Number, // 0–100
  breakdown: {
    reviewCompletion: Number,
    reinforcementAccuracy: Number,
    engagementDiversity: Number,
    interactionFrequency: Number,
    selfReflectionUsage: Number
  }
};

// --------------------
// 7. OrchestratorEvent (for scoring over time)
// --------------------
const OrchestratorEvent = {
  _id: ObjectId,
  userId: ObjectId,
  triggeredAt: Date,               // When the orchestrator decided something
  triggerSource: "daily_scan" | "missed_review" | "manual_request" | "plan_start",
  actionType: "schedule_review" | "reinforce" | "remind" | "adjust_plan",
  contentId: ObjectId,             // Optional, if linked to a resource
  chatSessionId: ObjectId,         // Optional, if chat-based
  reviewScheduleId: ObjectId,      // Optional, if it led to one
  reinforcementItemIds: [ObjectId],// Optional, if auto-generated
  reason: String,                  // Optional, e.g., "low score", "missed 2 reviews"
  meta: Object,                    // Optional JSON: anything dynamic (e.g., pacing context, time-of-day rules)
  status: "executed" | "skipped" | "failed", // Helpful for monitoring
  createdAt: Date,
  updatedAt: Date
};
