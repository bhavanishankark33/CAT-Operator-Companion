function Header() {
  return (
    <header className="border-b border-white/10 bg-[#0e1319]">
      <div className="mx-auto flex max-w-[1600px] items-center justify-between px-6 py-4">

        {/* LEFT */}
        <div className="flex items-center gap-4">
          <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-[#f5c400] text-xl font-black text-black">
            CAT
          </div>

          <div>
            <h1 className="text-lg font-bold">
              Operator Companion
            </h1>

            <p className="text-xs text-gray-500">
              Machine intelligence & operator support
            </p>
          </div>
        </div>

        {/* RIGHT */}
        <div className="flex items-center gap-6">

          <div className="hidden text-right sm:block">
            <p className="text-sm font-medium">
              EXCAVATOR 320
            </p>

            <p className="text-xs text-gray-500">
              Machine #CAT-320-07
            </p>
          </div>

          <div className="flex items-center gap-2 rounded-full border border-green-500/20 bg-green-500/10 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-green-400">
            <span className="h-2 w-2 rounded-full bg-green-400" />
            System Active
          </div>

          <div className="text-sm text-gray-400">
            10:42 AM
          </div>

        </div>
      </div>
    </header>
  );
}

export default Header;