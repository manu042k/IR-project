export enum SortMethod {
  RELEVANCE = 'relevance',
  SCORE = 'score',
  TIME = 'time',
}

export interface SearchParams {
  query: string;
  count?: number;
  sort_method?: SortMethod;
  weight_relevance?: number;
  weight_score?: number;
  weight_time?: number;
  use_pagerank?: boolean;
}

export interface SearchResultItem {
  id: string;
  elasticsearch_score: number;
  subreddit: string;
  subreddit_url: string;
  title: string;
  post_text: string;
  post_id: string;
  score: number;
  num_comments: number;
  post_url: string;
  sport: string;
  upvote_ratio: number;
  awards: number;
  time: string;
  pagerank_score: number;
}

export interface SearchResponse {
  status: string;
  message: string;
  count: number;
  query: string;
  sort_method: string;
  use_pagerank: boolean;
  data: SearchResultItem[];
}

export interface ApiResponse {
  status: string;
  message: string;
}
