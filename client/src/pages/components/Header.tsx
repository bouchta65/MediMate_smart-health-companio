import { Button } from "@/components/ui/button"
import { Heart, Phone, Mail, MapPin, Facebook, Twitter, Instagram, Linkedin } from "lucide-react"
import { Link } from 'react-router-dom';
import ThemeToggle from "@/components/ThemeToggle";

export default function HeaderCompo() {
    return (
        <div className=" flex flex-col bg-gray-50">

            {/* Header */}
            <header className="bg-white border-b border-blue-100 shadow-sm">
                <div className="container mx-auto px-4 lg:px-6">
                    <div className="flex items-center justify-between h-16">
                        {/* Logo and Brand */}
                        <div className="flex items-center space-x-3">
                            <div className="flex items-center justify-center w-10 h-10 bg-blue-600 rounded-lg">
                                <Heart className="h-6 w-6 text-white" />
                            </div>
                            <div className="flex flex-col">
                                <span className="text-xl font-bold text-blue-900">Medimate</span>
                                <span className="text-xs text-blue-600 font-medium">Healthcare Solutions</span>
                            </div>
                        </div>

                        {/* Navigation */}
                        <nav className="hidden md:flex items-center space-x-8">
                            <Link href="/" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
                                Home
                            </Link>
                            <Link href="/" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
                                Services
                            </Link>
                            <Link href="/" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
                                Doctors
                            </Link>
                            <Link href="/" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
                                About
                            </Link>
                            <Link href="/" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
                                Contact
                            </Link>
                        </nav>

                        {/* Auth Buttons */}
                        <div className="flex items-center space-x-3">
                            <Button
                                variant="outline"
                                className="bg-white text-blue-600 border-blue-200 hover:bg-blue-50 hover:text-blue-700"
                            >
                                Login
                            </Button>
                            <Button className="bg-blue-600 hover:bg-blue-700 text-white">Register</Button>
                            <ThemeToggle />
                        </div>

                    </div>
                </div>
            </header>
        </div>
    )
}