import React from 'react';
import { LineChart, Line, ResponsiveContainer } from 'recharts';
import { ArrowUpRight, DollarSign } from 'lucide-react';

const data = [
  { name: 'Jan', uv: 4000 },
  { name: 'Feb', uv: 3000 },
  { name: 'Mar', uv: 2000 },
  { name: 'Apr', uv: 2780 },
  { name: 'May', uv: 1890 },
  { name: 'Jun', uv: 2390 },
  { name: 'Jul', uv: 3490 },
];

const TradingBotGraphic: React.FC = () => {
  return (
    <div className="relative flex flex-col items-center justify-center p-4">
      {/* Phone Container */}
      <div className="relative w-64 h-96 bg-black rounded-[2.5rem] border-4 border-gold shadow-2xl overflow-hidden z-10">
        {/* Phone Screen */}
        <div className="absolute inset-2 bg-gray-900 rounded-[2rem] flex flex-col p-4">
          {/* Top Bar */}
          <div className="flex justify-between items-center mb-4">
            <span className="text-white text-sm font-semibold">9:41 AM</span>
            <div className="flex items-center space-x-1">
              <span className="text-white text-xs">5G</span>
              <div className="w-4 h-2 border border-white rounded-[2px]">
                <div className="w-3 h-full bg-white rounded-[1px]"></div>
              </div>
            </div>
          </div>

          {/* App Content */}
          <div className="flex-grow flex flex-col justify-between">
            <div className="text-center mb-4">
              <h2 className="text-silver text-lg font-bold">AI Trading Bot</h2>
              <p className="text-gold text-3xl font-extrabold mt-1 flex items-center justify-center">
                <DollarSign className="h-6 w-6 mr-1" /> 12,345.67
              </p>
              <p className="text-green-400 text-sm flex items-center justify-center mt-1">
                <ArrowUpRight className="h-4 w-4 mr-1" /> +2.5% Today
              </p>
            </div>

            {/* Chart */}
            <div className="flex-grow w-full h-32">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data} margin={{ top: 5, right: 10, left: 10, bottom: 5 }}>
                  <Line type="monotone" dataKey="uv" stroke="#FFD700" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Action Button */}
            <button className="mt-4 w-full bg-gold text-black py-2 rounded-xl font-bold text-lg shadow-lg hover:bg-yellow-500 transition-colors">
              Activate Bot
            </button>
          </div>
        </div>
        {/* Notch */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-24 h-6 bg-black rounded-b-xl z-20"></div>
      </div>

      {/* Lake Reflection */}
      <div className="relative w-64 h-48 mt-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black opacity-70 blur-sm"></div>
        <div className="absolute inset-0 transform scale-y-[-1] opacity-50">
          <div className="relative w-full h-full bg-black rounded-[2.5rem] border-4 border-gold shadow-2xl overflow-hidden">
            <div className="absolute inset-2 bg-gray-900 rounded-[2rem] flex flex-col p-4">
              <div className="flex justify-between items-center mb-4">
                <span className="text-white text-sm font-semibold"></span>
                <div className="flex items-center space-x-1">
                  <span className="text-white text-xs"></span>
                  <div className="w-4 h-2 border border-white rounded-[2px]">
                    <div className="w-3 h-full bg-white rounded-[1px]"></div>
                  </div>
                </div>
              </div>
              <div className="flex-grow flex flex-col justify-between">
                <div className="text-center mb-4">
                  <h2 className="text-silver text-lg font-bold"></h2>
                  <p className="text-gold text-3xl font-extrabold mt-1 flex items-center justify-center">
                    <DollarSign className="h-6 w-6 mr-1" />
                  </p>
                  <p className="text-green-400 text-sm flex items-center justify-center mt-1">
                    <ArrowUpRight className="h-4 w-4 mr-1" />
                  </p>
                </div>
                <div className="flex-grow w-full h-32">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data} margin={{ top: 5, right: 10, left: 10, bottom: 5 }}>
                      <Line type="monotone" dataKey="uv" stroke="#FFD700" strokeWidth={2} dot={false} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
                <button className="mt-4 w-full bg-gold text-black py-2 rounded-xl font-bold text-lg shadow-lg"></button>
              </div>
            </div>
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-24 h-6 bg-black rounded-b-xl"></div>
          </div>
        </div>
        {/* Simple ripple effect using pseudo-element */}
        <div className="absolute inset-x-0 bottom-0 h-1/3 bg-gradient-to-t from-black to-transparent opacity-80"></div>
      </div>
    </div>
  );
};

export default TradingBotGraphic;