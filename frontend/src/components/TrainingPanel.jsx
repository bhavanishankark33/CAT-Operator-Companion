function TrainingPanel({ data }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-[#11171e] p-6">

      {/* HEADER */}
      <div className="mb-5">
        <p className="text-xs font-semibold uppercase tracking-widest text-gray-500">
          Training & Coaching
        </p>

        <h2 className="mt-1 text-xl font-bold">
          Your next improvement
        </h2>
      </div>

      {/* COACHING CARD */}
      <div className="rounded-xl border border-white/10 bg-[#0c1117] p-5">

        <div className="flex items-start gap-4">

          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-[#f5c400] font-bold text-black">
            {data.step}
          </div>

          <div>

            <p className="font-semibold">
              {data.title}
            </p>

            <p className="mt-2 text-sm leading-6 text-gray-400">
              {data.description}
            </p>

            <button
              className="mt-4 rounded-lg bg-white/10 px-4 py-2 text-sm font-medium transition hover:bg-white/15"
            >
              Learn more
            </button>

          </div>

        </div>

      </div>

    </div>
  );
}

export default TrainingPanel;