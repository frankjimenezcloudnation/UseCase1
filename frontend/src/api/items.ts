import { api } from "@/api/client";

export interface Item {
  id: number;
  name: string;
  description: string | null;
}

export interface ItemCreate {
  name: string;
  description?: string | null;
}

export const itemsApi = {
  list: () => api.get<Item[]>("/items"),
  create: (payload: ItemCreate) => api.post<Item>("/items", payload),
  remove: (id: number) => api.del<void>(`/items/${id}`),
};
