import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";

function clean(html: string) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export async function GET(req: NextRequest) {
  const q = req.nextUrl.searchParams.get("q")?.trim();
  if (!q) return NextResponse.json({ error: "Missing q" }, { status: 400 });

  try {
    const response = await fetch(
      "https://html.duckduckgo.com/html/?q=" + encodeURIComponent(q),
      { headers: { "user-agent": "NETX-Web/1.0" }, cache: "no-store" }
    );

    if (!response.ok) {
      return NextResponse.json({ error: "Search provider returned " + response.status }, { status: 502 });
    }

    const html = await response.text();
    const results = [...html.matchAll(/result__a[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi)]
      .slice(0, 10)
      .map((match, index) => ({
        id: index + 1,
        title: clean(match[2]),
        url: match[1],
        summary: "Web result returned by NETX search.",
      }));

    return NextResponse.json({ query: q, results });
  } catch {
    return NextResponse.json({ error: "Research request failed" }, { status: 502 });
  }
}
