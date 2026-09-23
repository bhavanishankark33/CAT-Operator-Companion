function ActivityPanel({ data }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-[#11171e] p-6">

      {/* HEADER */}
      <div className="mb-5">
        <p className="text-xs font-semibold uppercase tracking-widest text-gray-500">
          Recent Activity
        </p>

        <h2 className="mt-1 text-xl font-bold">
          What the companion noticed
        </h2>
      </div>

      {/* ACTIVITY LIST */}
      <div className="space-y-4">

        {data.map((activity) => (
          <div
            key={activity.time}
            className="flex items-center justify-between border-b border-white/5 pb-3 last:border-0"
          >

            <div className="flex items-center gap-3">

              <span
                className={`h-2 w-2 rounded-full ${
                  activity.status === "normal"
                    ? "bg-green-400"
                    : activity.status === "attention"
                    ? "bg-yellow-400"
                    : "bg-red-400"
                }`}
              />

              <span className="text-sm text-gray-300">
                {activity.text}
              </span>

            </div>

            <span className="text-xs text-gray-600">
              {activity.time}
            </span>

          </div>
        ))}

      </div>

    </div>
  );
}

export default ActivityPanel;