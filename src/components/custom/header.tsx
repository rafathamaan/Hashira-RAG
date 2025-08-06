import { ThemeToggle } from "./theme-toggle";
import { Link } from "react-router-dom";    

export const Header = () => {
  return (
    <header className="flex items-center justify-between px-2 sm:px-4 py-2 bg-background text-black dark:text-white w-full">
      <div className="flex items-center space-x-2">
        <div className="flex items-center space-x-4 sm:space-x-2">
        <ThemeToggle />
      </div>
        <Link to="http://localhost:8501/">
          <img
            src="src/assets/fonts/images/hashira-logo-full.svg"
            alt="Hashira Logo"
            className="h-24 w-24 cursor-pointer hover:opacity-80 transition-opacity"
            draggable={false}
          />
        </Link>

        {/* Optional: Add a site title or tagline here */}
        {/* <span className="text-lg font-semibold hidden sm:inline">YourAppName</span> */}
      </div>

      {/* Right section: Theme toggle */}
      
    </header>
  );
};
