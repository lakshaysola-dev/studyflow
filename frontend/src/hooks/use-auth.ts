"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { api, getToken, setToken } from "@/lib/api";
import type { Token, User } from "@/lib/types";

export function useMe() {
  return useQuery({
    queryKey: ["me"],
    queryFn: () => api<User>("/auth/me"),
    enabled: typeof window !== "undefined" && !!getToken(),
    retry: false,
  });
}

export function useLogin() {
  const qc = useQueryClient();
  const router = useRouter();
  return useMutation({
    mutationFn: (body: { email: string; password: string }) =>
      api<Token>("/auth/login", { method: "POST", body: JSON.stringify(body) }),
    onSuccess: (data) => {
      setToken(data.access_token);
      qc.setQueryData(["me"], data.user);
      router.replace("/");
    },
  });
}

export function useRegister() {
  const qc = useQueryClient();
  const router = useRouter();
  return useMutation({
    mutationFn: (body: { email: string; password: string; full_name: string }) =>
      api<Token>("/auth/register", { method: "POST", body: JSON.stringify(body) }),
    onSuccess: (data) => {
      setToken(data.access_token);
      qc.setQueryData(["me"], data.user);
      router.replace("/");
    },
  });
}

export function useLogout() {
  const qc = useQueryClient();
  const router = useRouter();
  return () => {
    setToken(null);
    qc.clear();
    router.replace("/login");
  };
}
