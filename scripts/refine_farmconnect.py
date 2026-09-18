from pathlib import Path

p = Path('/home/ubuntu/farmconnect/client/src/App.tsx')
s = p.read_text()

replacements = []
replacements.append((
'const roleOptions = ["Consumer Demo", "Farmer Demo", "FPO Demo", "Bulk Buyer Demo", "Admin Demo"];',
'''const roleOptions = ["Consumer Demo", "Farmer Demo", "FPO Demo", "Bulk Buyer Demo", "Admin Demo"];
const roleAccess: Record<string, string[]> = {
  "Consumer Demo": ["/dashboard", "/marketplace", "/orders", "/product", "/communication", "/group-buying", "/repeat-orders", "/payments", "/ratings", "/logistics", "/notifications", "/disputes", "/settings"],
  "Farmer Demo": ["/dashboard", "/marketplace", "/orders", "/product", "/communication", "/demand-forecast", "/inventory", "/logistics", "/route-optimization", "/group-buying", "/repeat-orders", "/export", "/notifications", "/ratings", "/disputes", "/settings"],
  "FPO Demo": ["/dashboard", "/marketplace", "/orders", "/product", "/communication", "/demand-forecast", "/inventory", "/logistics", "/route-optimization", "/group-buying", "/repeat-orders", "/export", "/bulk-buyers", "/notifications", "/ratings", "/disputes", "/settings"],
  "Bulk Buyer Demo": ["/dashboard", "/marketplace", "/orders", "/product", "/communication", "/group-buying", "/repeat-orders", "/export", "/bulk-buyers", "/payments", "/ratings", "/logistics", "/notifications", "/disputes", "/settings"],
  "Admin Demo": ["/dashboard", "/marketplace", "/orders", "/product", "/communication", "/demand-forecast", "/inventory", "/logistics", "/route-optimization", "/group-buying", "/repeat-orders", "/export", "/bulk-buyers", "/payments", "/ratings", "/disputes", "/notifications", "/admin", "/settings"],
};
function canAccess(role: string, path: string) {
  const root = `/${path.split("/")[1] || "dashboard"}`;
  return (roleAccess[role] || roleAccess["Consumer Demo"]).includes(root);
}
function downloadText(filename: string, content: string, type = "text/plain") {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}'''))
replacements.append((
'const ctx = { role, setRole, notify, orders, setOrders, cartCount, setCartCount };\n  const pageTitle = titleForPath(location);',
'const ctx = { role, setRole, notify, orders, setOrders, cartCount, setCartCount };\n  const pageTitle = titleForPath(location);\n  const accessDenied = !canAccess(role, location);'))
replacements.append(('<main className="mx-auto max-w-[1500px] p-5 lg:p-8"><Switch>', '<main className="mx-auto max-w-[1500px] p-5 lg:p-8">{accessDenied ? <AccessDeniedPage role={role} path={location} /> : <Switch>'))
replacements.append(('<Route component={DashboardPage} /></Switch></main>', '<Route component={DashboardPage} /></Switch>}</main>'))
replacements.append(('function Sidebar() { const [location, navigate] = useLocation(); const { role, setRole, cartCount } = useDemo();', 'function Sidebar() { const [location, navigate] = useLocation(); const { role, setRole, cartCount, notify } = useDemo();'))
replacements.append(('{group.items.map(item => { const active = location === item.path;', '{group.items.filter(item => canAccess(role, item.path)).map(item => { const active = location === item.path;'))
replacements.append(('onClick={() => navigate(item.path)}', 'onClick={() => canAccess(role, item.path) ? navigate(item.path) : notify(`The ${item.label} workspace is not available for ${role.replace(" Demo", "")} demo.`)}'))
replacements.append(('function titleForPath(path: string)', '''function AccessDeniedPage({ role, path }: { role: string; path: string }) { const [, navigate] = useLocation(); return <div className="mx-auto max-w-2xl py-20"><Card className="rounded-2xl border-[#e2ebe0] bg-white text-center shadow-[0_8px_25px_rgba(34,74,47,.04)]"><CardContent className="p-10"><div className="mx-auto flex size-14 items-center justify-center rounded-2xl bg-[#fff3d7] text-[#b17d20]"><ShieldCheck className="size-7" /></div><h2 className="mt-6 text-2xl font-semibold tracking-[-.04em] text-[#173b2d]">Workspace access is restricted</h2><p className="mx-auto mt-3 max-w-md text-sm leading-6 text-[#70867b]">{role} does not have access to <strong>{titleForPath(path)}</strong>. Switch demo roles or return to an allowed workspace.</p><div className="mt-6 flex justify-center gap-2"><Button variant="outline" className="rounded-xl border-[#d7e4d5] bg-white" onClick={() => navigate("/settings")}>Switch role</Button><Button className="rounded-xl bg-[#1f7a4d] hover:bg-[#155d3a]" onClick={() => navigate("/dashboard")}>Back to overview</Button></div></CardContent></Card></div> }
function titleForPath(path: string)'''))
replacements.append(('onClick={() => notify("Report exported as a demo PDF") }', 'onClick={() => { downloadText("farmconnect-overview.csv", "Metric,Value\\nFarmers connected,2480\\nOrders this month,1286\\nDemand signal,+18.6%\\nActive deliveries,24", "text/csv"); notify("Overview report downloaded"); } }'))
replacements.append(('function NotificationsPage() { const { notify } = useDemo(); const items = [[', 'function NotificationsPage() { const { notify } = useDemo(); const [readAll, setReadAll] = useState(false); const [signals, setSignals] = useState([true, true, true, true]); const items = [['))
replacements.append(('onClick={() => notify("All notifications marked as read") }', 'onClick={() => { setReadAll(true); notify("All notifications marked as read"); } }'))
replacements.append(('<div className="text-sm font-semibold text-[#527061]">{title as string}</div>', '<div className={`text-sm font-semibold ${readAll ? "text-[#8aa095]" : "text-[#527061]"}`}>{title as string}</div>'))
replacements.append(('{["Order updates","Demand signals","Low stock alerts","New market opportunities"].map(x => <div key={x} className="flex items-center justify-between rounded-xl bg-white/70 p-3"><span className="text-xs font-medium text-[#587267]">{x}</span><div className="h-5 w-9 rounded-full bg-[#4d9b62] p-0.5"><div className="ml-4 size-4 rounded-full bg-white shadow-sm" /></div></div>)}', '{["Order updates","Demand signals","Low stock alerts","New market opportunities"].map((x, i) => <button key={x} onClick={() => setSignals(current => current.map((value, index) => index === i ? !value : value))} className="flex w-full items-center justify-between rounded-xl bg-white/70 p-3 text-left"><span className="text-xs font-medium text-[#587267]">{x}</span><div className={`h-5 w-9 rounded-full p-0.5 ${signals[i] ? "bg-[#4d9b62]" : "bg-[#cbd8cb]"}`}><div className={`size-4 rounded-full bg-white shadow-sm transition ${signals[i] ? "ml-4" : "ml-0"}`} /></div></button>)}'))
replacements.append(('function VoiceAssistant() { const { notify } = useDemo();', 'function VoiceAssistant() { const { notify } = useDemo(); const [, navigate] = useLocation();'))
replacements.append(('onClick={() => { notify(`Assistant: ${command}`); setOpen(false); }}', 'onClick={() => { const commandRoutes: Record<string, string> = { "Show today’s orders": "/orders", "Add tomatoes": "/marketplace", "Show stock": "/inventory", "Check demand": "/demand-forecast" }; notify(`Assistant: ${command}`); setOpen(false); if (commandRoutes[command]) navigate(commandRoutes[command]); }}'))

for old, new in replacements:
    if old not in s:
        raise SystemExit(f'missing pattern: {old[:100]}')
    s = s.replace(old, new, 1)
p.write_text(s)
print('patched', p)
