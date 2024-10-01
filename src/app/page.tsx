import { CopilotPopup } from "@copilotkit/react-ui";
import { CopilotKitProvider } from "@/components/CopilotKitProvider";

export default function Home() {
  return (
    <div>
      <CopilotKitProvider>
        <CopilotPopup
          labels={{
            title: "Popup Assistant",
            initial: "Need any help?",
          }}
        />
      </CopilotKitProvider>
    </div>
  );
}
