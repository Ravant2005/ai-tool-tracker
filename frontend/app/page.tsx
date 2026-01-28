import ToolsClient from '@/components/ToolsClient';

// Force dynamic rendering - prevent static generation
export const dynamic = 'force-dynamic';

export default function Home() {
    return <ToolsClient />;
}