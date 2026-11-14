export type Route = { kind: 'catalog' } | { kind: 'subject'; subjectId: string; localHash: string } | { kind: 'not-found' };
const legacy = /^#\/(?:chuong\/[1-6]|con-so|thi-thu|can-on|keyword|lam-bai|ket-qua|nguon)$/;
export function subjectHref(subjectId: string, localHash = '#/'): string {
  const suffix = localHash.replace(/^#\/?/, '');
  return `#/mon/${subjectId}${suffix ? '/' + suffix : ''}`;
}
export function legacyRedirect(hash: string): string | null { return legacy.test(hash) ? subjectHref('tthcm', hash) : null; }
export function resolveRoute(hash: string): Route {
  if (!hash || hash === '#/' || hash === '#') return { kind: 'catalog' };
  const match = hash.match(/^#\/mon\/([a-z0-9-]+)(?:\/(.*))?$/);
  return match ? { kind: 'subject', subjectId: match[1], localHash: '#/' + (match[2] ?? '') } : { kind: 'not-found' };
}
export function scopeSubjectLinks(html: string, subjectId: string): string {
  return html.replace(/<a\b([^>]*?)href="(#[^"]*)"([^>]*)>/g, (whole, before: string, href: string, after: string) => {
    if ((before + after).includes('data-global') || href.startsWith('#/mon/') || !href.startsWith('#/')) return whole;
    return `<a${before}href="${subjectHref(subjectId, href)}"${after}>`;
  });
}
