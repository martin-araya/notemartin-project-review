// Hooks tipados para usar en lugar de useDispatch / useSelector crudos.
// Trampa del ecosistema #3: si se importan desde "react-redux" en lugar de
// estos hooks, los tipos son any y el comportamiento cambia.

import { useDispatch, useSelector } from "react-redux";
import type { RootState, AppDispatch } from "../index.js";

export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector = <T>(selector: (state: RootState) => T): T =>
  useSelector(selector);