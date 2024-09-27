import { CopilotPopup } from "@copilotkit/react-ui";

export default function Home() {
  return (
    <div>
      <CopilotPopup
        labels={{
          title: "Popup Assistant",
          initial: "Need any help?",
        }}
      />
    </div>
  );
}
