import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";

import Header from "./components/Header";
import StatusBadge from "./components/StatusBadge";
import MetricCard from "./components/MetricCard";
import LiveCompanion from "./components/LiveCompanion";
import PerformancePanel from "./components/PerformancePanel";
import ActivityPanel from "./components/ActivityPanel";
import TrainingPanel from "./components/TrainingPanel";

import { machineState } from "./services/mockData";

function App() {
  return (
    <div className="min-h-screen bg-[#0b0f14] text-white">

      {/* HEADER */}
      <Header />

      {/* MAIN */}
      <main className="mx-auto max-w-[1600px] px-6 py-6">

        {/* TOP STATUS */}
        <section className="mb-6 grid gap-4 md:grid-cols-3">

          <MetricCard
  title="Machine Status"
  value={machineState.machine.status}
  subtitle={machineState.machine.subtitle}
  status={machineState.machine.systemStatus}
/>

<MetricCard
  title="Current Task"
  value={machineState.task.name}
  subtitle={`Cycle ${machineState.task.currentCycle} of ${machineState.task.totalCycles}`}
  status={machineState.task.status}
/>

<MetricCard
  title="Safety Status"
  value={machineState.safety.status}
  subtitle={machineState.safety.subtitle}
  status={machineState.safety.level}
/>

        </section>

        {/* MAIN GRID */}
        <section className="grid gap-6 lg:grid-cols-3">

          {/* LIVE COMPANION */}
          <LiveCompanion data={machineState.companion} />

          {/* PERFORMANCE PANEL */}
          <PerformancePanel data={machineState.performance} />

        </section>

        {/* LOWER GRID */}
        <section className="mt-6 grid gap-6 lg:grid-cols-2">

          {/* RECENT ACTIVITY */}
         <ActivityPanel data={machineState.activity} />


          {/* TRAINING */}
          <TrainingPanel data={machineState.training} />

        </section>

      </main>

      {/* VOICE BUTTON */}
      <button
        className="fixed bottom-6 right-6 flex items-center gap-3 rounded-full bg-[#f5c400] px-6 py-4 font-bold text-black shadow-2xl transition hover:scale-105"
        onClick={() => alert("Voice Companion coming next!")}
      >
        <span className="text-xl">
          🎙
        </span>

        Talk to Companion
      </button>

    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);