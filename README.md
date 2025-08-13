<p align="center">
    <img src="assets/logo.png" alt="Micro Break Logo" width="200"/>
    <!-- <h1>Micro Breaks</h1> -->
</p>

## Features

- Guided micro-breaks to improve productivity and well-being
- Customizable work and break intervals
- Notifications and reminders for scheduled breaks
- Simple, user-friendly interface
- Progress tracking and daily usage statistics

## Use Case

Micro Break is designed for professionals, students, and anyone who spends extended periods working at a computer. By encouraging regular, guided breaks, the app helps reduce eye strain, prevent repetitive stress injuries, and maintain mental focus throughout the day.

## Business Justification

Prolonged periods of uninterrupted computer work can lead to decreased productivity, increased fatigue, and higher risk of health issues such as carpal tunnel syndrome and burnout. Micro Break addresses these challenges by promoting healthy work habits, which can result in:
- Improved employee well-being and job satisfaction
- Reduced absenteeism due to health-related issues
- Enhanced overall productivity and work quality

## Getting Started

### Prerequisites

- Python 3.8 or higher

### Installation

```bash
git clone https://github.com/your-org/micro-break-vibe-coding.git
cd micro-break-vibe-coding
pip install -r requirements.txt
```

### Running the App

```bash
python src\main.py
```

## Deployment Process (Windows)

To deploy Micro Break as a Windows application:

1. **Install Dependencies**  
   Ensure Python and all required packages are installed using the provided `requirements.txt`.

2. **Package the Application**  
   Use a tool like [PyInstaller](https://www.pyinstaller.org/) to bundle the app into an executable:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed src\main.py
   ```
   This will generate a standalone `.exe` file in the `dist` directory.

3. **Distribute the Executable**  
   Share the generated `.exe` file with users. Optionally, create an installer using tools like [Inno Setup](https://jrsoftware.org/isinfo.php) for a smoother installation experience.

4. **Run the Application**  
   Double-click the `.exe` file to launch Micro Break on any compatible Windows machine.

## Usage

1. Set your preferred work and break durations.
2. Start your work session.
3. Follow the guided micro-breaks when prompted.
4. Track your progress throughout the day.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Acknowledgements

- Developed by Team Take A Break  
- Cognizant Vibe Coding 2025

## License

Copyright © 2025 Cognizant Vibe Coding, Team Take A Break. All rights reserved.

This software and its associated documentation files (the "Software") are the exclusive property of Cognizant. Unauthorized copying, distribution, modification, sublicensing, or use of any part of the Software is strictly prohibited without the express written permission of the copyright holders.

The Software is provided for internal use within Cognizant only. No part of the Software may be reproduced, stored in a retrieval system, or transmitted in any form or by any means—electronic, mechanical, photocopying, recording, or otherwise—without prior written consent.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For licensing inquiries, please contact the project owner.

