import { CopilotKitProvider } from "@/components/CopilotKitProvider";
import { BasicAgentChat } from "@/components/BasicAgentChat";
import { CopilotChat } from "@copilotkit/react-ui";

export default function Home() {
  return (
    <CopilotKitProvider agent="basic_agent">
      {/* <BasicAgentChat /> */}
      <CopilotChat
        labels={{
          title: "Popup Assistant",
          initial: "Need any help?",
        }}
      />
    </CopilotKitProvider>
  );
}
