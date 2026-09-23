export const machineState = {
  machine: {
    name: "EXCAVATOR 320",
    id: "CAT-320-07",
    status: "Operating",
    systemStatus: "normal",
    subtitle: "Hydraulic systems normal",
  },

  task: {
    name: "Trench Digging",
    currentCycle: 18,
    totalCycles: 42,
    status: "normal",
  },

  safety: {
    status: "Clear",
    level: "normal",
    subtitle: "No active hazards detected",
  },

  companion: {
    status: "Monitoring",
    statusLevel: "normal",

    message: "Operation looks good",

    description:
      "Your current digging cycle is within the expected operating range. Continue at the current pace.",

    machineState: "Digging",

    nextExpected: "Lift → Swing",

    cycleQuality: "Good",
  },

  performance: {
    efficiency: 87,
    averageCycle: 31.4,
    targetCycle: 30.0,

    improvement: {
      level: "attention",
      title: "Small improvement opportunity",
      description:
        "Swing time is slightly above the expected range.",
    },
  },

  activity: [
    {
      time: "10:41:52",
      text: "Dig cycle completed",
      status: "normal",
    },
    {
      time: "10:41:21",
      text: "Bucket load within target",
      status: "normal",
    },
    {
      time: "10:40:48",
      text: "Swing time slightly high",
      status: "attention",
    },
    {
      time: "10:40:16",
      text: "Safe operating zone confirmed",
      status: "normal",
    },
  ],

  training: {
    step: 1,
    title: "Improve swing transition",

    description:
      "Try beginning the swing immediately after the bucket reaches the recommended lift position.",
  },
};