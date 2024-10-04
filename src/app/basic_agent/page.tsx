import { CopilotKitProvider } from "@/components/CopilotKitProvider";
import { MoreBasicAgentChat } from "@/components/MoreBasicAgentChat";
import { BasicAgentChat } from "@/components/BasicAgentChat";
import { CopilotChat } from "@copilotkit/react-ui";

import "../globals.css";

export default function Home() {
  return (
    <CopilotKitProvider agent="basic_agent">
      <MoreBasicAgentChat />
      {/* <BasicAgentChat /> */}
      {/* <CopilotChat
        labels={{
          title: "Weather Assistant",
          initial: "Where would you like to go?",
        }}
      /> */}
    </CopilotKitProvider>
  );
}
