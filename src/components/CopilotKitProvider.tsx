"use client";

import "@copilotkit/react-ui/styles.css";

import { CopilotKit } from "@copilotkit/react-core";

export function CopilotKitProvider({ children }: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit">
      {children}
    </CopilotKit>
  )
}