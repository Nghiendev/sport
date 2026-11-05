import { useDeferredValue, useMemo, useState } from "react";
import termsData from "./data/terms.json";
import sourcesData from "./data/sources.json";
import type { Source, Term } from "./types";

const terms = termsData as Term[];
const sources = sourcesData as Source[];

type View = "home" | "glossary" | "sources";

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

export default function App() {
  const [view, setView] = useState<View>("home");
  const [group, setGroup] = useState<string>("Tất cả");
  const [query, setQuery] = useState("");
  const [selectedId, setSelectedId] = useState<string | null>(terms[0]?.id ?? null);
  const deferredQuery = useDeferredValue(query);

  const groups = useMemo(() => {
    const map = new Map<string, number>();
    for (const t of terms) {
      const g = t.group || "Khác";
      map.set(g, (map.get(g) ?? 0) + 1);
    }
    return [...map.entries()];
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
        <nav className="nav">
          <button
            type="button"
            className={view === "home" ? "active" : ""}
            onClick={() => setView("home")}
          >
            Tổng quan
          </button>
          <button
            type="button"
            className={view === "glossary" ? "active" : ""}
            onClick={() => setView("glossary")}
          >
            Từ điển
          </button>
          <button
            type="button"
            className={view === "sources" ? "active" : ""}
            onClick={() => setView("sources")}
          >
            Nguồn
          </button>
        </nav>
      </header>

      {view === "home" ? (
        <>
          <section className="hero">
            <div className="eyebrow">Open glossary · Việt / Anh</div>
            <h1>Ngôn ngữ MMA</h1>
            <p>
              Bộ khung thuật ngữ võ thuật tổng hợp — định nghĩa thao tác, vị trí, luật và
              ngôn ngữ phân tích, theo tinh thần FIFA Football Language: một “ngôn ngữ
              chung” để học, dạy và bình luận trận đấu.
            </p>
            <div className="hero-cta">
              <button type="button" className="btn btn-primary" onClick={() => setView("glossary")}>
                Mở từ điển
              </button>
              <button type="button" className="btn" onClick={() => setView("sources")}>
                Xem nguồn tham khảo
              </button>
            </div>
          </section>

          <section className="section">
            <div className="stats">
              <div className="stat">
                <strong>{terms.length}</strong>
                <span>mục từ</span>
              </div>
              <div className="stat">
                <strong>{groups.length}</strong>
                <span>nhóm chuyên môn</span>
              </div>
              <div className="stat">
                <strong>{sources.length}</strong>
                <span>nguồn đối chiếu</span>
              </div>
            </div>

            <h2>Khám phá theo nhóm</h2>
            <p className="section-lead">
              Chọn một lĩnh vực để xem các định nghĩa vận hành — giống cách FIFA chia
              Football Language theo tình huống trên sân.
            </p>
            <div className="category-grid">
              {groups.map(([name, count]) => (
                <button
                  key={name}
                  type="button"
                  className="category-card"
                  onClick={() => openGroup(name)}
                >
                  <span className="count">{count} mục</span>
                  <h3>{name}</h3>
                  <p>{GROUP_BLURBS[name] ?? "Thuật ngữ chuyên môn MMA."}</p>
                </button>
              ))}
            </div>
          </section>
        </>
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
                  <span className="id">{t.id}</span>
                  <span className="vi">{t.vi}</span>
                  <span className="en">{t.en}</span>
                </button>
              ))}
              {filtered.length === 0 ? (
                <p className="section-lead">Không có mục khớp bộ lọc.</p>
              ) : null}
            </div>

            {selected ? (
              <aside className="detail">
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
        MMA Language · {terms.length} mục · dữ liệu biên tập từ spreadsheet công khai
      </footer>
    </div>
  );
}
