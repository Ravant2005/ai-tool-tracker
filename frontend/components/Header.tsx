import { Sparkles } from 'lucide-react';

export default function Header() {
    return (
        <header className="bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg">
            <div className="container mx-auto px-4 py-6">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <div className="bg-white p-2 rounded-lg">
                            <Sparkles className="w-6 h-6 text-purple-600" />
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold">AI Tool Tracker</h1>
                            <p className="text-sm text-purple-100">
                                Discover trending AI tools daily
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
}