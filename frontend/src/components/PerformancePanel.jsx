function PerformancePanel({ data }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-[#11171e] p-6">

      <div className="mb-5">
        <p className="text-xs font-semibold uppercase tracking-widest text-gray-500">
          Performance
        </p>

        <h2 className="mt-1 text-xl font-bold">
          Current shift
        </h2>
      </div>

      <div className="space-y-5">

        {/* CYCLE EFFICIENCY */}
        <div>
          <div className="mb-2 flex justify-between text-sm">
            <span className="text-gray-400">
              Cycle efficiency
            </span>

            <span className="font-semibold">
              {data.efficiency}%
            </span>
          </div>

          <div className="h-2 overflow-hidden rounded-full bg-white/10">
            <div
              className="h-full rounded-full bg-[#f5c400] transition-all duration-500"
              style={{ width: `${data.efficiency}%` }}
            />
          </div>
        </div>

        {/* CYCLE METRICS */}
        <div className="grid grid-cols-2 gap-3">

          <div className="rounded-xl bg-[#0c1117] p-4">
            <p className="text-xs text-gray-500">
              Avg. Cycle
            </p>

            <p className="mt-2 text-xl font-bold">
              {data.averageCycle}s
            </p>
          </div>

          <div className="rounded-xl bg-[#0c1117] p-4">
            <p className="text-xs text-gray-500">
              Target
            </p>

            <p className="mt-2 text-xl font-bold">
              {data.targetCycle}s
            </p>
          </div>

        </div>

        {/* IMPROVEMENT */}
        <div className="rounded-xl border border-yellow-500/20 bg-yellow-500/5 p-4">

          <p className="text-sm font-semibold text-yellow-300">
            {data.improvement.title}
          </p>

          <p className="mt-1 text-xs leading-5 text-gray-500">
            {data.improvement.description}
          </p>

        </div>

      </div>
    </div>
  );
}

export default PerformancePanel;