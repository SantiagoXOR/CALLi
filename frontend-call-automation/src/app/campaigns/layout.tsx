import Layout from "@/components/Layout";

export default function CampaignsLayout({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element {
  return <Layout>{children}</Layout>;
}
