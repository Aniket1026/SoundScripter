import { create } from "zustand";

interface ModalStoreType {
    isOpen: boolean;

    toggleModal(): void;
}

const useModalStore = create<ModalStoreType>((set, get) => ({
    isOpen: false,

    toggleModal: () => set(() => ({ isOpen: !get().isOpen })),
}));

export default useModalStore;