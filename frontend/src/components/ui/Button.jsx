export function Button({ children, className = "", ...props }) {
  return (
    <button
      className={`rounded-md bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-700 ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
