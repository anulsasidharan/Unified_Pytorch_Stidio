import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Navbar } from '@/components/layout/Navbar';
import { DashboardPage } from '@/pages/DashboardPage';
import { LearnPage } from '@/pages/LearnPage';
import { PracticeListPage } from '@/pages/PracticeListPage';
import { PracticePage } from '@/pages/PracticePage';
import { ImportPage } from '@/pages/ImportPage';
import { RevisionPage } from '@/pages/RevisionPage';
import { TrackPage } from '@/pages/TrackPage';
import { TopicDetailPage } from '@/pages/TopicDetailPage';
import { AssistantPage } from '@/pages/AssistantPage';
function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppLayout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/learn" element={<LearnPage />} />
          <Route path="/learn/:topicSlug" element={<TopicDetailPage />} />
          <Route path="/practice" element={<PracticeListPage />} />
          <Route path="/practice/:questionSlug" element={<PracticePage />} />
          <Route path="/track" element={<TrackPage />} />
          <Route path="/revision" element={<RevisionPage />} />
          <Route path="/import" element={<ImportPage />} />
          <Route path="/assistant" element={<AssistantPage />} />
        </Routes>
      </AppLayout>
    </BrowserRouter>
  );
}

export default App;
