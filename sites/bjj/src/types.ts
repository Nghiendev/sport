export type Video = {
  kind: "attack" | "defense" | "extra";
  title: string;
  videoId: string;
  url: string;
};

export type Skill = {
  id: string;
  name: string;
  nameEn: string;
  level: string;
  summary: string;
  videos: Video[];
};

export type Position = {
  id: string;
  label: string;
  x: number;
  y: number;
  role: "top" | "bottom" | "neutral" | "finish";
};

export type PositionEdge = {
  from: string;
  to: string;
  label: string;
  kind: "advance" | "recover" | "scramble";
};

export type Chain = {
  id: string;
  title: string;
  summary: string;
  skillIds: string[];
};

export type SkillLink = {
  from: string;
  to: string;
  label: string;
};

export type GraphData = {
  positions: Position[];
  positionEdges: PositionEdge[];
  chains: Chain[];
  skillLinks: SkillLink[];
};
