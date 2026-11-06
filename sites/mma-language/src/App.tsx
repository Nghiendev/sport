import { useDeferredValue, useMemo, useState, type ReactNode } from "react";
import termsData from "./data/terms.json";
import sourcesData from "./data/sources.json";
import proposalsData from "./data/proposals.json";
import notesData from "./data/notes.json";
import type { MatNote, Proposal, Source, Term } from "./types";
import {
  GroupIcon,
  IconBook,
  IconChart,
  IconDumbbell,
  IconHome,
  IconInfo,
  IconLayers,
  IconLink,
  IconPlay,
  IconSearch,
} from "./components/Icons";

const terms = termsData as Term[];
const sources = sourcesData as Source[];
const proposals = proposalsData as Proposal[];
const notes = notesData as MatNote[];

type View =
  | "home"
  | "glossary"
  | "themes"
  | "proposals"
  | "notes"
  | "method"
  | "video"
  | "drills"
  | "sources"
  | "about";

type NavItem = {
  id: View;
  label: string;
  icon: ReactNode;
};

const NAV: NavItem[] = [
  { id: "home", label: "Tổng quan", icon: <IconHome size={16} /> },
  { id: "glossary", label: "Từ điển", icon: <IconBook size={16} /> },
  { id: "themes", label: "Nhóm chủ đề", icon: <IconLayers size={16} /> },
  { id: "proposals", label: "Đề xuất", icon: <IconSearch size={16} /> },
  { id: "notes", label: "Ghi chép thảm", icon: <IconDumbbell size={16} /> },
  { id: "method", label: "Phương pháp", icon: <IconChart size={16} /> },
  { id: "video", label: "Video ví dụ", icon: <IconPlay size={16} /> },
  { id: "sources", label: "Nguồn", icon: <IconLink size={16} /> },
  { id: "about", label: "Về dự án", icon: <IconInfo size={16} /> },
];

const GROUP_BLURBS: Record<string, string> = {
  "Không gian giao đấu và chiến thuật": "Range, timing, pressure và cách đọc pha.",
  "Tư thế và bộ pháp": "Stance, guard, footwork và góc đứng.",
  "Đòn tay và phòng thủ đánh đứng": "Jab, cross, hook và các kiểu phòng thủ.",
  "Đá gối và chỏ": "Kick, knee, elbow trong striking.",
  "Áp sát tranh tay và vật lồng": "Clinch, underhook, cage wrestling.",
  "Vào vật chống vật và chuyển tiếp": "Takedown, sprawl, transition.",
  "Vị trí địa chiến và hệ guard": "Mount, side, guard và biến thể.",
  "Thoát thế đảo thế đánh trên sàn": "Escape, sweep, ground-and-pound.",
  "Khóa siết và tín hiệu chịu thua": "Submission, choke, tap.",
  "Huấn luyện dụng cụ và khẩu lệnh": "Pad, bag, corner language.",
  "Tổ chức trận đấu luật và kết quả": "Rounds, fouls, decision, stoppage.",
  "Thống kê và ngôn ngữ tường thuật": "Significant strikes, control time.",
  "Hạng cân và hồ sơ võ sĩ": "Weight classes, reach, record.",
};

const PLACEHOLDERS: Partial<
  Record<View, { title: string; lead: string; bullets: string[] }>
> = {
  method: {
    title: "Phương pháp phân tích",
    lead: "Khung cách đọc trận MMA bằng ngôn ngữ chung — nội dung chi tiết sẽ bổ sung sau.",
    bullets: [
      "Đọc pha theo striking → clinch → takedown → ground",
      "Phân biệt hành động trên bóng / ngoài bóng (áp lực, góc, nhịp)",
      "Checklist quan sát cho HLV, VĐV và bình luận viên",
      "Ma trận thuật ngữ theo cấp độ (cơ bản → nâng cao)",
    ],
  },
  video: {
    title: "Video ví dụ",
    lead: "Mỗi khái niệm sẽ gắn clip minh họa ngắn để làm rõ định nghĩa vận hành.",
    bullets: [
      "Playlist theo nhóm: jab, underhook, guard pass…",
      "Cặp video: đúng kỹ thuật vs lỗi phổ biến",
      "Slow-motion + chú thích thuật ngữ Việt–Anh",
      "Nhúng YouTube / clip tự quay trên thảm",
    ],
  },
  drills: {
    title: "Luyện tập & bài tập ngôn ngữ",
    lead: "Bài tập giúp nhớ và dùng đúng thuật ngữ khi tập / phân tích.",
    bullets: [
      "Quiz flashcard Việt ↔ Anh",
      "Nhận diện pha trên video → chọn đúng mục từ",
      "Bài viết corner instruction 30 giây",
      "Checklist warm-up vocab theo buổi tập",
    ],
  },
  about: {
    title: "Về dự án MMA Language",
    lead: "Bộ từ vựng vận hành mở để học và phân tích võ thuật tổng hợp.",
    bullets: [
      "Nguồn biên tập: Đinh Quốc Dũng — MMA Hà Đông",
      "Mục tiêu: thống nhất cách gọi giữa HLV, VĐV, truyền thông",
      "Từ điển chính + đề xuất chờ duyệt + ghi chép trên thảm",
      "Roadmap: video, drill, sâu hơn theo bộ môn",
    ],
  },
};

function ComingSoon({ view }: { view: View }) {
  const data = PLACEHOLDERS[view];
  if (!data) return null;
  return (
    <section className="section">
      <div className="coming-soon">
        <div className="coming-badge">Đang dựng · nội dung sẽ vá sau</div>
        <h2>{data.title}</h2>
        <p className="section-lead">{data.lead}</p>
        <ul className="coming-list">
          {data.bullets.map((b) => (
            <li key={b}>{b}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export default function App() {
  const [view, setView] = useState<View>("home");
  const [group, setGroup] = useState<string>("Tất cả");
  const [query, setQuery] = useState("");
  const [selectedId, setSelectedId] = useState<string | null>(terms[0]?.id ?? null);
  const [discipline, setDiscipline] = useState("Tất cả");
  const [proposalQuery, setProposalQuery] = useState("");
  const deferredQuery = useDeferredValue(query);
  const deferredProposalQuery = useDeferredValue(proposalQuery);

  const groups = useMemo(() => {
    const map = new Map<string, number>();
    for (const t of terms) {
      const g = t.group || "Khác";
      map.set(g, (map.get(g) ?? 0) + 1);
    }
    return [...map.entries()];
  }, []);

  const disciplines = useMemo(() => {
    const set = new Set<string>();
    for (const p of proposals) if (p.discipline) set.add(p.discipline);
    return [...set].sort((a, b) => a.localeCompare(b, "vi"));
  }, []);

  const filtered = useMemo(() => {
    const q = deferredQuery.trim().toLowerCase();
    return terms.filter((t) => {
      if (group !== "Tất cả" && t.group !== group) return false;
      if (!q) return true;
      return (
        t.id.toLowerCase().includes(q) ||
        t.vi.toLowerCase().includes(q) ||
        t.en.toLowerCase().includes(q) ||
        t.def.toLowerCase().includes(q)
      );
    });
  }, [deferredQuery, group]);

  const filteredProposals = useMemo(() => {
    const q = deferredProposalQuery.trim().toLowerCase();
    return proposals.filter((p) => {
      if (discipline !== "Tất cả" && p.discipline !== discipline) return false;
      if (!q) return true;
      return [p.vi, p.en, p.original, p.proposed, p.discipline, p.relatedId]
        .join(" ")
        .toLowerCase()
        .includes(q);
    });
  }, [deferredProposalQuery, discipline]);

  const selected = terms.find((t) => t.id === selectedId) ?? null;

  function openGroup(name: string) {
    setGroup(name);
    setView("glossary");
    const first = terms.find((t) => t.group === name);
    if (first) setSelectedId(first.id);
  }

  return (
    <div className="app">
      <header className="topbar">
        <button type="button" className="logo" onClick={() => setView("home")}>
          MMA <span>Language</span>
        </button>
        <nav className="nav" aria-label="Menu chính">
          {NAV.map((item) => (
            <button
              key={item.id}
              type="button"
              className={view === item.id ? "active" : ""}
              onClick={() => setView(item.id)}
            >
              <span className="nav-ico">{item.icon}</span>
              {item.label}
            </button>
          ))}
        </nav>
      </header>

      {view === "home" ? (
        <>
          <section className="hero">
            <div className="hero-copy">
              <div className="eyebrow">Open glossary · Việt / Anh</div>
              <h1>Ngôn ngữ MMA</h1>
              <p>
                Bộ khung thuật ngữ võ thuật tổng hợp — định nghĩa thao tác, vị trí, luật và
                ngôn ngữ phân tích trận đấu.
              </p>
              <div className="hero-cta">
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={() => setView("glossary")}
                >
                  <IconBook size={18} /> Mở từ điển
                </button>
                <button type="button" className="btn" onClick={() => setView("proposals")}>
                  <IconSearch size={18} /> Xem đề xuất mới
                </button>
              </div>
            </div>
            <div className="hero-visual" aria-hidden>
              <div className="hero-orb">
                <GroupIcon group="Đòn tay và phòng thủ đánh đứng" size={42} />
              </div>
              <div className="hero-orb delay">
                <GroupIcon group="Vị trí địa chiến và hệ guard" size={36} />
              </div>
              <div className="hero-orb delay2">
                <GroupIcon group="Áp sát tranh tay và vật lồng" size={34} />
              </div>
            </div>
          </section>

          <section className="section">
            <div className="stats">
              <div className="stat">
                <strong>{terms.length}</strong>
                <span>mục từ đã biên</span>
              </div>
              <div className="stat">
                <strong>{proposals.length}</strong>
                <span>đề xuất chờ duyệt</span>
              </div>
              <div className="stat">
                <strong>{notes.length}</strong>
                <span>ghi chép thảm</span>
              </div>
              <div className="stat">
                <strong>{sources.length}</strong>
                <span>nguồn đối chiếu</span>
              </div>
            </div>

            <h2>Khám phá theo nhóm</h2>
            <p className="section-lead">
              Mỗi thẻ là một “chương” ngôn ngữ — chọn để vào từ điển đã lọc sẵn.
            </p>
            <div className="category-grid">
              {groups.map(([name, count]) => (
                <button
                  key={name}
                  type="button"
                  className="category-card"
                  onClick={() => openGroup(name)}
                >
                  <span className="cat-icon">
                    <GroupIcon group={name} />
                  </span>
                  <span className="count">{count} mục</span>
                  <h3>{name}</h3>
                  <p>{GROUP_BLURBS[name] ?? "Thuật ngữ chuyên môn MMA."}</p>
                </button>
              ))}
            </div>
          </section>
        </>
      ) : null}

      {view === "themes" ? (
        <section className="section">
          <h2>Nhóm chủ đề</h2>
          <p className="section-lead">
            Bản đồ các miền ngôn ngữ trong từ điển đã biên tập.
          </p>
          <div className="category-grid">
            {groups.map(([name, count]) => (
              <button
                key={name}
                type="button"
                className="category-card"
                onClick={() => openGroup(name)}
              >
                <span className="cat-icon">
                  <GroupIcon group={name} />
                </span>
                <span className="count">{count} mục</span>
                <h3>{name}</h3>
                <p>{GROUP_BLURBS[name] ?? "Thuật ngữ chuyên môn MMA."}</p>
              </button>
            ))}
          </div>
        </section>
      ) : null}

      {view === "glossary" ? (
        <section className="section">
          <h2>Từ điển MMA Việt – Anh</h2>
          <p className="section-lead">
            Tìm theo tiếng Việt, tiếng Anh hoặc mã mục. Chọn một dòng để xem giải nghĩa đầy
            đủ.
          </p>
          <div className="toolbar">
            <input
              className="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Tìm jab, clinch, rear naked choke, sweep…"
            />
            <select
              className="select"
              value={group}
              onChange={(e) => setGroup(e.target.value)}
            >
              <option value="Tất cả">Tất cả nhóm</option>
              {groups.map(([name]) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </select>
          </div>

          <div className="layout">
            <div className="term-list">
              {filtered.map((t) => (
                <button
                  key={t.id}
                  type="button"
                  className={`term-row${selectedId === t.id ? " active" : ""}`}
                  onClick={() => setSelectedId(t.id)}
                >
                  <span className="term-row-top">
                    <span className="term-mini-ico">
                      <GroupIcon group={t.group} size={18} />
                    </span>
                    <span className="id">{t.id}</span>
                    <span className="vi">{t.vi}</span>
                  </span>
                  <span className="en">{t.en}</span>
                </button>
              ))}
              {filtered.length === 0 ? (
                <p className="section-lead">Không có mục khớp bộ lọc.</p>
              ) : null}
            </div>

            {selected ? (
              <aside className="detail">
                <div className="detail-icon">
                  <GroupIcon group={selected.group} size={32} />
                </div>
                <div className="code">{selected.id}</div>
                <h2>{selected.vi}</h2>
                <p className="en-title">{selected.en}</p>
                <p className="def">{selected.def}</p>
                <div className="meta-grid">
                  {selected.group ? (
                    <div className="meta-item">
                      <strong>Nhóm</strong>
                      {selected.group}
                    </div>
                  ) : null}
                  {selected.context ? (
                    <div className="meta-item">
                      <strong>Bối cảnh sử dụng</strong>
                      {selected.context}
                    </div>
                  ) : null}
                  {selected.function ? (
                    <div className="meta-item">
                      <strong>Chức năng</strong>
                      {selected.function}
                    </div>
                  ) : null}
                </div>
                <div className="chip-row">
                  <span className="chip">VI → EN</span>
                  <span className="chip">{selected.group || "MMA"}</span>
                </div>
              </aside>
            ) : (
              <aside className="detail empty">
                <p>Chọn một mục từ danh sách để xem định nghĩa.</p>
              </aside>
            )}
          </div>
        </section>
      ) : null}

      {view === "proposals" ? (
        <section className="section">
          <h2>Đề xuất biên tập</h2>
          <p className="section-lead">
            {proposals.length} mục đang <strong>chờ duyệt</strong> — bổ sung theo bộ môn (Muay,
            Boxing, BJJ, Wrestling…). Chưa nhập vào từ điển chính.
          </p>
          <div className="toolbar">
            <input
              className="search"
              value={proposalQuery}
              onChange={(e) => setProposalQuery(e.target.value)}
              placeholder="Tìm kru, liver shot, double leg…"
            />
            <select
              className="select"
              value={discipline}
              onChange={(e) => setDiscipline(e.target.value)}
            >
              <option value="Tất cả">Tất cả bộ môn</option>
              {disciplines.map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
          </div>
          <div className="proposal-grid">
            {filteredProposals.map((p, idx) => (
              <article key={`${p.original}-${p.vi}-${idx}`} className="proposal-card">
                <div className="proposal-top">
                  <span className="status-pill">{p.status || "Chờ duyệt"}</span>
                  {p.discipline ? <span className="discipline-pill">{p.discipline}</span> : null}
                  {p.relatedId ? <span className="related-pill">{p.relatedId}</span> : null}
                </div>
                <h3>{p.vi || p.original || "Đề xuất chưa đặt tên Việt"}</h3>
                <p className="en-line">{p.en || p.original}</p>
                {p.proposed ? <p>{p.proposed}</p> : null}
                {p.current ? (
                  <p className="current-line">
                    <strong>Hiện tại:</strong> {p.current}
                  </p>
                ) : null}
                {p.source ? (
                  <a href={p.source} target="_blank" rel="noreferrer">
                    Nguồn / lý do
                  </a>
                ) : null}
              </article>
            ))}
            {filteredProposals.length === 0 ? (
              <p className="section-lead">Không có đề xuất khớp bộ lọc.</p>
            ) : null}
          </div>
        </section>
      ) : null}

      {view === "notes" ? (
        <section className="section">
          <h2>Ghi chép trên thảm</h2>
          <p className="section-lead">
            Từ hoặc câu nghe được khi tập — dùng để bổ sung từ điển sau khi biên tập.
          </p>
          <div className="notes-grid">
            {notes.map((n, idx) => (
              <article key={`${n.heard}-${idx}`} className="note-card">
                <h3>{n.heard}</h3>
                {n.situation ? <p>{n.situation}</p> : null}
                <div className="note-meta">
                  {n.date ? <span>{n.date}</span> : null}
                  {n.link ? (
                    <a href={n.link} target="_blank" rel="noreferrer">
                      Xem clip
                    </a>
                  ) : null}
                </div>
              </article>
            ))}
          </div>
        </section>
      ) : null}

      {view === "method" || view === "video" || view === "drills" || view === "about" ? (
        <ComingSoon view={view} />
      ) : null}

      {view === "sources" ? (
        <section className="section">
          <h2>Nguồn tham khảo</h2>
          <p className="section-lead">
            Các số trong ngoặc vuông ở phần giải nghĩa (nếu có) dẫn về nguồn trong bảng
            này.
          </p>
          <div className="sources">
            {sources.map((s) => (
              <article key={s.id} className="source-card">
                <div className="sid">{s.id}</div>
                <h3>{s.title || s.id}</h3>
                {s.scope ? <p>{s.scope}</p> : null}
                {s.url ? (
                  <a href={s.url} target="_blank" rel="noreferrer">
                    Mở tài liệu
                  </a>
                ) : null}
              </article>
            ))}
          </div>
        </section>
      ) : null}

      <footer className="footer">
        Nguồn: Đinh Quốc Dũng — MMA Hà Đông
      </footer>
    </div>
  );
}
