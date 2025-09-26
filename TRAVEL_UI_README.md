# 🌍 AI Travel Planner Web Interface

A beautiful web interface for interacting with AWS Bedrock Agent to generate personalized travel plans.

## ✨ Features

- **Interactive Form**: Easy-to-use web form for travel planning requests
- **Real-time AI Generation**: Connects directly to your Bedrock Agent via `agentcore`
- **Beautiful Visualization**: Displays travel plans in a stunning, responsive HTML format
- **Comprehensive Planning**: Includes transportation, accommodation, activities, and daily itineraries
- **Budget Tracking**: Shows detailed cost breakdowns and budget compliance
- **Mobile Responsive**: Works perfectly on desktop, tablet, and mobile devices

## 🚀 Quick Start

### Prerequisites

1. **agentcore CLI**: Make sure you have `agentcore` installed and configured
2. **Python 3**: Required for the web server
3. **AWS Bedrock Agent**: Your Bedrock Agent should be properly configured

### Running the Interface

1. **Start the server**:
   ```bash
   ./start_travel_ui.sh
   ```

2. **Open your browser**:
   Navigate to `http://localhost:8080`

3. **Plan your trip**:
   - Fill out the travel form
   - Click "Generate My Travel Plan"
   - Wait for the AI to create your personized itinerary
   - View your beautiful travel plan!

## 📁 Files Overview

- `travel_planner_ui.html` - Main web interface with form and results display
- `travel_server.py` - Python backend server that executes agentcore commands
- `start_travel_ui.sh` - Convenience script to start the server
- `trip_plan_visualization.html` - Standalone HTML visualization (example output)

## 🔧 How It Works

1. **User Input**: Fill out the comprehensive travel form
2. **Prompt Generation**: The form data is converted into a natural language prompt
3. **Agent Execution**: The server executes: `agentcore invoke '{"prompt": "..."}'`
4. **Response Processing**: JSON response from Bedrock Agent is parsed
5. **Beautiful Display**: Results are formatted into a stunning HTML presentation

## 📝 Example Usage

The interface pre-fills with an example "romantic weekend in Paris" request:

- **Destination**: Paris, France
- **Budget**: $1200
- **Interests**: Art, Fine Dining
- **Trip Type**: Romantic Getaway
- **Duration**: Weekend (2-3 days)

## 🎨 Features Highlight

### Form Features
- **Smart Date Picker**: Prevents past dates, auto-adjusts end date
- **Interest Tags**: Click to select/deselect travel interests
- **Trip Type Selection**: Romantic, Family, Solo, Friends, Business, Honeymoon
- **Budget Tracking**: Numeric input with validation
- **Additional Requests**: Free-form text for special requirements

### Results Display
- **Trip Overview**: Key metrics in an attractive card layout
- **Transportation**: Flight details with pricing and timing
- **Accommodation**: Hotel information with ratings
- **Activities**: Curated experiences with locations and ratings  
- **Daily Itinerary**: Time-based schedule for each day
- **Cost Breakdown**: Total costs with budget comparison
- **AI Summary**: Personalized narrative about the trip

### Design Elements
- **Gradient Backgrounds**: Modern, professional appearance
- **Responsive Grid**: Adapts to any screen size
- **Interactive Elements**: Hover effects and smooth transitions
- **Emoji Integration**: Fun, visual icons throughout
- **Color-coded Sections**: Easy navigation and visual hierarchy

## 🛠️ Customization

### Modifying the Server

Edit `travel_server.py` to:
- Change port number (default: 8080)
- Add authentication
- Implement caching
- Add request logging
- Handle different agent commands

### Styling Changes

Edit the CSS in `travel_planner_ui.html` to:
- Change color scheme
- Modify layout
- Add animations
- Customize fonts
- Update responsive breakpoints

### Form Modifications

Update the HTML form to:
- Add new input fields
- Change interest categories
- Modify trip types
- Add validation rules
- Include additional form sections

## 🔍 Troubleshooting

### Common Issues

1. **"agentcore command not found"**
   - Ensure agentcore is installed and in your PATH
   - Try running `which agentcore` to verify

2. **"Connection refused"**
   - Make sure the server is running on port 8080
   - Check if another service is using the port

3. **"Request timed out"**
   - Bedrock Agent responses can take time
   - Check your AWS credentials and permissions
   - Verify your agent configuration

4. **"Invalid JSON response"**
   - Check agentcore command output format
   - Verify your Bedrock Agent is configured correctly

### Server Logs

The server provides detailed logging:
- Request processing
- agentcore command execution
- Error details
- Response parsing

## 📱 Mobile Experience

The interface is fully responsive and provides an excellent experience on:
- **Desktop**: Full-featured form and results display
- **Tablet**: Optimized layout with touch-friendly controls
- **Mobile**: Compact design with all functionality preserved

## 🚀 Advanced Usage

### Command Line Testing

Test your agentcore directly:
```bash
agentcore invoke '{"prompt": "Plan a romantic weekend in Paris, budget $1200, interests: art and fine dining"}'
```

### Batch Processing

You can modify the server to handle multiple requests or save results to files.

### Integration

The server can be extended to integrate with:
- Database storage for trip plans
- User authentication systems
- Payment processing
- Booking APIs
- Email notifications

## 🎯 Next Steps

1. **Try the Interface**: Start with the pre-filled Paris example
2. **Create Your Own Plan**: Fill out the form with your dream destination
3. **Explore Results**: Review the detailed itinerary and costs
4. **Customize**: Modify the styling or add new features
5. **Share**: The generated HTML can be saved and shared

Enjoy planning your perfect trip with AI! 🧳✈️