function StatusBadge({ status, children }) {
  const styles = {
    normal: "bg-green-500/10 text-green-400 border-green-500/20",
    attention: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
    critical: "bg-red-500/10 text-red-400 border-red-500/20",
  };

  const dotStyles = {
    normal: "bg-green-400",
    attention: "bg-yellow-400",
    critical: "bg-red-400",
  };

  return (
    <span
      className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wide ${
        styles[status]
      }`}
    >
      <span
        className={`h-2 w-2 rounded-full ${dotStyles[status]}`}
      />

      {children}
    </span>
  );
}

export default StatusBadge;