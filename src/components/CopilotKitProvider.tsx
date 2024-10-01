"use client";

import "@copilotkit/react-ui/styles.css";

import { CopilotKit } from "@copilotkit/react-core";

type CopilotKitProviderProps = Readonly<{
  agent?: string;
  children: React.ReactNode;
}>

export function CopilotKitProvider(props: CopilotKitProviderProps) {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit" {...props} />
  )
}