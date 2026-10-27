// Recebe o cadastro do pop-up e repassa para os dois webhooks.
// Rodar no servidor evita bloqueio de CORS no navegador.

const WEBHOOKS = [
  "https://hook.us2.make.com/fkeoxrgwsfwmyt3ed9sfpucypjze2f8a",
  "https://unnichat.com.br/a/start/3M6Un15lTbpX67g9hkzQ",
];

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "method_not_allowed" });
  }

  let lead = req.body;
  if (typeof lead === "string") {
    try { lead = JSON.parse(lead); } catch (_) { lead = {}; }
  }
  lead = lead || {};

  if (!lead.email || !lead.nome || !lead.telefone) {
    return res.status(400).json({ ok: false, error: "missing_fields" });
  }

  const payload = JSON.stringify({
    ...lead,
    ip: (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || undefined,
    user_agent: req.headers["user-agent"],
  });

  const results = await Promise.allSettled(
    WEBHOOKS.map((url) =>
      fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: payload,
        signal: AbortSignal.timeout(8000),
      }).then((r) => ({ url, status: r.status }))
    )
  );

  const report = results.map((r, i) =>
    r.status === "fulfilled" ? r.value : { url: WEBHOOKS[i], error: String(r.reason) }
  );
  console.log("lead", lead.email, JSON.stringify(report));

  return res.status(200).json({ ok: true, report });
};
