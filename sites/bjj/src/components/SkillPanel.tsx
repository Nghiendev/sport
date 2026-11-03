import type { Skill, SkillLink } from "../types";
import { VideoEmbed } from "./VideoEmbed";

type Props = {
  skill: Skill | null;
  links: SkillLink[];
  skillMap: Record<string, Skill>;
  onSelectSkill: (id: string) => void;
};

const KIND_LABEL: Record<string, string> = {
  attack: "Tấn công / thực hiện",
  defense: "Phòng thủ / counter",
  extra: "Bổ sung",
};

export function SkillPanel({ skill, links, skillMap, onSelectSkill }: Props) {
  if (!skill) {
    return (
      <aside className="side-pane empty">
        <div>
          <p>Chọn một kỹ năng hoặc chuỗi để xem video và mối liên hệ.</p>
        </div>
      </aside>
    );
  }

  const related = links.filter((l) => l.from === skill.id || l.to === skill.id);
  const attack = skill.videos.find((v) => v.kind === "attack") ?? skill.videos[0];
  const defense = skill.videos.find((v) => v.kind === "defense");

  return (
    <aside className="side-pane">
      <h2>{skill.name}</h2>
      <div className="meta">
        {skill.nameEn ? `${skill.nameEn} · ` : ""}
        {skill.level || "—"}
      </div>
      {skill.summary ? <p className="summary">{skill.summary}</p> : null}

      {attack ? (
        <div className="video-block">
          <h4>{KIND_LABEL[attack.kind] ?? "Video"}</h4>
          <VideoEmbed videoId={attack.videoId} title={attack.title} />
        </div>
      ) : null}

      {defense ? (
        <div className="video-block">
          <h4>{KIND_LABEL.defense}</h4>
          <VideoEmbed videoId={defense.videoId} title={defense.title} />
        </div>
      ) : null}

      {related.length > 0 ? (
        <div className="related">
          <h4>Liên hệ kỹ năng</h4>
          <div className="skill-flow">
            {related.map((link) => {
              const otherId = link.from === skill.id ? link.to : link.from;
              const other = skillMap[otherId];
              const direction = link.from === skill.id ? "→" : "←";
              return (
                <button
                  key={`${link.from}-${link.to}-${link.label}`}
                  type="button"
                  className="chip"
                  onClick={() => onSelectSkill(otherId)}
                >
                  {direction} {other?.name ?? otherId}
                  <span style={{ opacity: 0.65 }}> · {link.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      ) : null}
    </aside>
  );
}
