import Navbar from "@/components/Navbar"

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-r from-blue-50 to-blue-100">
      <Navbar />
      {children}
    </div>
  )
}
