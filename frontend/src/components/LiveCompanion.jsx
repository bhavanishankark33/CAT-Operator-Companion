import StatusBadge from "./StatusBadge";

function LiveCompanion({ data }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-[#11171e] p-6 lg:col-span-2">

      {/* HEADER */}
      <div className="mb-5 flex items-center justify-between">

        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-gray-500">
            Live Companion
          </p>

          <h2 className="mt-1 text-xl font-bold">
            Operator guidance
          </h2>
        </div>

        <StatusBadge status={data.statusLevel}>
          {data.status}
        </StatusBadge>

      </div>

      {/* CURRENT GUIDANCE */}
      <div className="rounded-xl border border-green-500/20 bg-green-500/5 p-5">

        <div className="flex gap-4">

          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-green-500/10 text-green-400">
            ✓
          </div>

          <div>

            <p className="font-semibold text-green-300">
              {data.message}
            </p>

            <p className="mt-1 text-sm leading-6 text-gray-400">
              {data.description}
            </p>

          </div>

        </div>

      </div>

      {/* LIVE STATE */}
      <div className="mt-5 grid gap-4 sm:grid-cols-3">

        <div className="rounded-xl bg-[#0c1117] p-4">

          <p className="text-xs text-gray-500">
            Machine State
          </p>

          <p className="mt-2 font-semibold">
            {data.machineState}
          </p>

        </div>

        <div className="rounded-xl bg-[#0c1117] p-4">

          <p className="text-xs text-gray-500">
            Next Expected
          </p>

          <p className="mt-2 font-semibold">
            {data.nextExpected}
          </p>

        </div>

        <div className="rounded-xl bg-[#0c1117] p-4">

          <p className="text-xs text-gray-500">
            Cycle Quality
          </p>

          <p className="mt-2 font-semibold text-green-400">
            {data.cycleQuality}
          </p>

        </div>

      </div>

    </div>
  );
}

export default LiveCompanion;