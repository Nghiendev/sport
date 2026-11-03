import { useDeferredValue, useMemo, useState } from "react";
import skillsData from "./data/skills.json";
import graphData from "./data/graph.json";
import type { GraphData, Skill } from "./types";
import { PositionGraph } from "./components/PositionGraph";
import { SkillPanel } from "./components/SkillPanel";

const skills = skillsData as Skill[];
const graph = graphData as GraphData;

type Tab = "map" | "chains" | "library";

const POSITION_SKILLS: Record<string, string[]> = {
  standing: ["collar-tie", "underhook", "double-leg", "single-leg", "guard-pull"],
  guard_bottom: ["closed-guard-bottom", "triangle-choke", "armbar", "hip-bump-sweep"],
  guard_top: ["closed-guard-top", "knee-cut-pass", "toreando-pass", "over-under-pass"],
  half: ["standard-half-guard", "old-school-half-sweep", "crossface-underhook-pass"],
  turtle: ["turtle-position", "granby-roll", "sit-out-escape", "rear-mount"],
  side_top: ["side-control", "americana", "kimura", "knee-drive-mount"],
  kob: ["knee-on-belly", "knee-drive-mount"],
  mount: ["mount-position", "armbar", "ezekiel-choke", "upa-escape"],
  back: ["rear-mount", "rear-naked-choke", "bow-and-arrow-choke", "rear-mount-escape"],
  finish: ["rear-naked-choke", "triangle-choke", "armbar", "americana"],
};

export default function App() {
  const [tab, setTab] = useState<Tab>("map");
  const [selectedSkillId, setSelectedSkillId] = useState<string | null>("triangle-choke");
  const [activeChainId, setActiveChainId] = useState(graph.chains[0]?.id ?? "");
  const [activePositionId, setActivePositionId] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);

  const skillMap = useMemo(
    () => Object.fromEntries(skills.map((s) => [s.id, s])) as Record<string, Skill>,
    []
  );

  const selectedSkill = selectedSkillId ? skillMap[selectedSkillId] ?? null : null;
  const activeChain = graph.chains.find((c) => c.id === activeChainId) ?? graph.chains[0];

  const filteredSkills = useMemo(() => {
    const q = deferredQuery.trim().toLowerCase();
    if (!q) return skills.slice(0, 48);
    return skills
      .filter(
        (s) =>
          s.name.toLowerCase().includes(q) ||
          s.nameEn.toLowerCase().includes(q) ||
          s.id.includes(q)
      )
      .slice(0, 60);
  }, [deferredQuery]);

  function selectSkill(id: string) {
    setSelectedSkillId(id);
  }

  function selectPosition(id: string) {
    setActivePositionId(id);
    const first = POSITION_SKILLS[id]?.[0];
    if (first && skillMap[first]) setSelectedSkillId(first);
  }

  return (
    <div className="app">
      <header className="hero" id="top">
        <h1 className="brand">
          MAT<span>MAP</span>
        </h1>
        <p className="hero-lead">
          Bản đồ tương tác Brazilian Jiu-Jitsu — xem chuỗi chuyển vị trí, móc nối kỹ
          năng, và học trực tiếp qua video nhúng.
        </p>
        <div className="hero-actions">
          <button type="button" className="btn btn-primary" onClick={() => setTab("map")}>
            Mở bản đồ vị trí
          </button>
          <button type="button" className="btn" onClick={() => setTab("chains")}>
            Chuỗi tấn công
          </button>
          <button type="button" className="btn" onClick={() => setTab("library")}>
            Thư viện {skills.length} kỹ năng
          </button>
        </div>
      </header>

      <div className="layout">
        <main className="main-pane">
          <div className="toolbar">
            <div className="tabs" role="tablist">
              <button
                type="button"
                className={`tab${tab === "map" ? " active" : ""}`}
                onClick={() => setTab("map")}
              >
                Bản đồ
              </button>
              <button
                type="button"
                className={`tab${tab === "chains" ? " active" : ""}`}
                onClick={() => setTab("chains")}
              >
                Chuỗi
              </button>
              <button
                type="button"
                className={`tab${tab === "library" ? " active" : ""}`}
                onClick={() => setTab("library")}
              >
                Thư viện
              </button>
            </div>
            {tab === "library" ? (
              <input
                className="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Tìm kỹ năng (jab, triangle, escape…)"
              />
            ) : null}
          </div>

          {tab === "map" ? (
            <>
              <div className="legend">
                <span>
                  <i style={{ background: "#7eb6ff" }} /> Tiến công / pass
                </span>
                <span>
                  <i style={{ background: "#5ddea8" }} /> Thoát / sweep
                </span>
                <span>
                  <i style={{ background: "#ff8a4c" }} /> Scramble
                </span>
              </div>
              <PositionGraph
                graph={graph}
                activePositionId={activePositionId}
                onSelectPosition={selectPosition}
              />
              {activePositionId && POSITION_SKILLS[activePositionId] ? (
                <div className="skill-flow" style={{ marginTop: "1rem" }}>
                  {POSITION_SKILLS[activePositionId].map((id) => (
                    <button
                      key={id}
                      type="button"
                      className={`chip${selectedSkillId === id ? " active" : ""}`}
                      onClick={() => selectSkill(id)}
                    >
                      {skillMap[id]?.name ?? id}
                    </button>
                  ))}
                </div>
              ) : null}
            </>
          ) : null}

          {tab === "chains" ? (
            <>
              <div className="chain-list">
                {graph.chains.map((chain) => (
                  <button
                    key={chain.id}
                    type="button"
                    className={`chain-card${activeChainId === chain.id ? " active" : ""}`}
                    onClick={() => {
                      setActiveChainId(chain.id);
                      const first = chain.skillIds.find((id) => skillMap[id]);
                      if (first) setSelectedSkillId(first);
                    }}
                  >
                    <h3>{chain.title}</h3>
                    <p>{chain.summary}</p>
                  </button>
                ))}
              </div>
              {activeChain ? (
                <div className="skill-flow">
                  {activeChain.skillIds.map((id, idx) => {
                    const skill = skillMap[id];
                    if (!skill) return null;
                    return (
                      <span key={id} style={{ display: "contents" }}>
                        {idx > 0 ? <span className="chip-arrow">→</span> : null}
                        <button
                          type="button"
                          className={`chip${selectedSkillId === id ? " active" : ""}`}
                          onClick={() => selectSkill(id)}
                        >
                          {skill.name}
                        </button>
                      </span>
                    );
                  })}
                </div>
              ) : null}
            </>
          ) : null}

          {tab === "library" ? (
            <div className="skill-grid">
              {filteredSkills.map((skill) => (
                <button
                  key={skill.id}
                  type="button"
                  className={`skill-card${selectedSkillId === skill.id ? " active" : ""}`}
                  onClick={() => selectSkill(skill.id)}
                >
                  <strong>{skill.name}</strong>
                  <span>
                    {skill.nameEn || skill.id} {skill.level ? `· ${skill.level}` : ""}
                  </span>
                </button>
              ))}
            </div>
          ) : null}
        </main>

        <SkillPanel
          skill={selectedSkill}
          links={graph.skillLinks}
          skillMap={skillMap}
          onSelectSkill={selectSkill}
        />
      </div>

      <footer className="footer">
        MATMAP · dữ liệu từ <code>sport/bjj</code> · {skills.length} kỹ năng có video
      </footer>
    </div>
  );
}
