import type { GraphData, Position } from "../types";

const ROLE_FILL: Record<Position["role"], string> = {
  top: "#1f3a55",
  bottom: "#1f4034",
  neutral: "#2a332e",
  finish: "#4a1f24",
};

const EDGE_STROKE: Record<"advance" | "recover" | "scramble", string> = {
  advance: "#7eb6ff",
  recover: "#5ddea8",
  scramble: "#ff8a4c",
};

type Props = {
  graph: GraphData;
  activePositionId: string | null;
  onSelectPosition: (id: string) => void;
};

export function PositionGraph({ graph, activePositionId, onSelectPosition }: Props) {
  const byId = Object.fromEntries(graph.positions.map((p) => [p.id, p]));
  const w = 940;
  const h = 780;
  const nodeW = 148;
  const nodeH = 40;

  return (
    <div className="graph-wrap">
      <svg className="graph-svg" viewBox={`0 0 ${w} ${h}`} role="img" aria-label="Sơ đồ chuyển vị trí BJJ">
        {graph.positionEdges.map((edge, i) => {
          const a = byId[edge.from];
          const b = byId[edge.to];
          if (!a || !b) return null;
          const x1 = a.x + nodeW / 2;
          const y1 = a.y + nodeH;
          const x2 = b.x + nodeW / 2;
          const y2 = b.y;
          const mx = (x1 + x2) / 2;
          const my = (y1 + y2) / 2;
          return (
            <g key={`${edge.from}-${edge.to}-${i}`}>
              <line
                x1={x1}
                y1={y1}
                x2={x2}
                y2={y2}
                stroke={EDGE_STROKE[edge.kind]}
                strokeWidth={1.6}
                opacity={0.75}
              />
              <text className="edge-label" x={mx} y={my - 4} textAnchor="middle">
                {edge.label}
              </text>
            </g>
          );
        })}

        {graph.positions.map((pos) => {
          const active = pos.id === activePositionId;
          return (
            <g
              key={pos.id}
              className={`node-pos${active ? " active" : ""}`}
              onClick={() => onSelectPosition(pos.id)}
            >
              <rect
                x={pos.x}
                y={pos.y}
                width={nodeW}
                height={nodeH}
                rx={10}
                fill={ROLE_FILL[pos.role]}
                stroke={active ? "#d4ff3a" : "rgba(232,239,233,0.2)"}
                strokeWidth={active ? 2 : 1}
              />
              <text x={pos.x + nodeW / 2} y={pos.y + 25} textAnchor="middle">
                {pos.label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
