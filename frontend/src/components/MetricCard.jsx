function MetricCard({
  title,
  value,
  subtitle,
  status = "normal",
}) {
  const dotStyles = {
    normal: "bg-green-400",
    attention: "bg-yellow-400",
    critical: "bg-red-400",
  };

  return (
    <div className="rounded-2xl border border-white/10 bg-[#11171e] p-5 shadow-lg">

      <div className="mb-3 flex items-center justify-between">

        <p className="text-sm text-gray-400">
          {title}
        </p>

        <span
          className={`h-2.5 w-2.5 rounded-full ${dotStyles[status]}`}
        />

      </div>

      <p className="text-3xl font-bold tracking-tight">
        {value}
      </p>

      <p className="mt-1 text-sm text-gray-500">
        {subtitle}
      </p>

    </div>
  );
}

export default MetricCard;