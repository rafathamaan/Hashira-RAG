import { ThemeToggle } from "./theme-toggle";
import { Link } from "react-router-dom";    

export const Header = () => {
  return (
    <header className="flex items-center justify-between px-2 sm:px-4 py-2 bg-background text-black dark:text-white w-full">
      <div className="flex items-center space-x-2">
        <div className="flex items-center space-x-4 sm:space-x-2">
        <ThemeToggle />
      </div>
        <Link to="/">
          <img
            src="src/assets/fonts/images/hashira-logo-full.svg"
            alt="Hashira Logo"
            className="h-24 w-24 cursor-pointer hover:opacity-80 transition-opacity"
            draggable={false}
          />
        </Link>

        
      </div>      
    </header>
  );
};
