export function Card({ children, className = "" }) {
  return <section className={`rounded-xl bg-white p-4 shadow-sm ${className}`}>{children}</section>;
}
