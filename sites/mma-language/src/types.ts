export type Term = {
  id: string;
  vi: string;
  en: string;
  def: string;
  group: string;
  context: string;
  function: string;
};

export type Source = {
  id: string;
  title: string;
  scope: string;
  url: string;
};

export type Proposal = {
  relatedId: string;
  current: string;
  proposed: string;
  source: string;
  status: string;
  note: string;
  discipline: string;
  original: string;
  vi: string;
  en: string;
  group: string;
  context: string;
  function: string;
};

export type MatNote = {
  heard: string;
  situation: string;
  link: string;
  date: string;
};
