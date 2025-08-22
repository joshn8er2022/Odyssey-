import { MadeWithDyad } from "@/components/made-with-dyad";
import { SafeLavaLamp } from "@/components/ui/SafeLavaLamp";
import { Spotlight } from "@/components/ui/spotlight";
import { SplineScene } from "@/components/ui/splite";

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center relative bg-black text-white overflow-hidden">
      {/* Luxury fluid background - loaded safely */}
      <SafeLavaLamp />

      {/* Content Layout */}
      <div className="relative z-10 flex flex-col lg:flex-row items-center justify-center w-full max-w-7xl px-4 py-16">
        
        {/* Left Side - Text Content */}
        <div className="flex-1 text-center lg:text-left lg:pr-12">
          <Spotlight className="-top-40 left-0 md:left-20 md:-top-20 opacity-30" fill="gold" />
          <p className="uppercase tracking-widest text-gold text-sm mb-4">
            Exclusive AI Wealth Management
          </p>
          <h1 className="text-5xl md:text-7xl font-extrabold leading-tight mb-6 bg-clip-text text-transparent bg-gradient-to-b from-gold to-silver drop-shadow-lg">
            Elite Algorithmic Trading
          </h1>
          <p className="text-lg md:text-xl text-silver mb-8 max-w-xl mx-auto lg:mx-0">
            Experience the pinnacle of decentralized finance with our exclusive AI trading agent.
            Designed for high-net-worth investors seeking luxury, precision, and results.
          </p>
          <button className="px-8 py-4 bg-gold text-black font-bold text-lg rounded-full shadow-xl hover:bg-yellow-500 transition-all duration-300 transform hover:scale-105">
            Reserve Access
          </button>
        </div>

        {/* Right Side - 3D Trader Agent with Ripple Reflection */}
        <div className="flex-1 flex justify-center lg:justify-end relative mt-12 lg:mt-0">
          <div className="relative w-full max-w-md">
            {/* 3D Agent Container */}
            <div className="relative z-20 rounded-3xl overflow-hidden border-4 border-gold shadow-2xl">
              <SplineScene 
                scene="https://prod.spline.design/kZDDjO5HuC9GJUM2/scene.splinecode" 
                className="w-full h-[500px]"
              />
            </div>

            {/* Reflection in 'water' effect */}
            <div className="absolute top-full w-full h-[150px] mt-4 overflow-hidden">
              <div className="w-full h-full transform scale-y-[-1] opacity-50 blur-sm">
                <div className="rounded-3xl overflow-hidden border-4 border-gold shadow-2xl">
                  <SplineScene 
                    scene="https://prod.spline.design/kZDDjO5HuC9GJUM2/scene.splinecode" 
                    className="w-full h-[500px]"
                  />
                </div>
              </div>
              <div className="absolute inset-x-0 bottom-0 h-1/2 bg-gradient-to-t from-black/80 via-black/50 to-transparent" />
            </div>
          </div>
        </div>

      </div>

      <MadeWithDyad />
    </div>
  );
};

export default Index;