import { create } from "zustand";
import { SessionItem } from "@/models/session.model";

interface PopupState {
  isVisible: boolean;
  currentItem: Partial<SessionItem> | null;
  showPopup: (item: Partial<SessionItem>) => void;
  hidePopup: () => void;
}

export const usePopupStore = create<PopupState>((set) => ({
  isVisible: false,
  currentItem: null,
  showPopup: (item) => set({ isVisible: true, currentItem: item }),
  hidePopup: () => set({ isVisible: false, currentItem: null }),
}));
