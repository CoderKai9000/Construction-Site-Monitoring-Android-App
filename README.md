# Construction-Site-Monitoring-Android-App
Monitors Activity on any construction site by person, machinery and PPE detection, sending alerts to admin on PPE non compliance, workforce graph plotting and overtime report generation and "zone-tagger",

## HOW TO RUN???

### Dashboard:
intall all the required dependencies

```
python app.py {OR} python3 app.py
```

### Android App
Open `Android_app` in Android Studio ->  Gradle Sync -> Gradle Build -> run on connected device.


### IMPORTANT INFO!!!! 
download the service-key json file from https://drive.google.com/file/d/1Hhjo1bBbHsMIEN3R7uFY1x3eTv2kYv2_/view?usp=sharing

and replace this in the dashboard folder. Also update app.py to include the path of the new json.

# **Construction activity monitoring using QIDK**

## Project Overview:

The Construction Site Monitoring project uses computer vision and machine learning to improve safety on construction sites by tracking safety gear, workers, and machines. It provides real-time detection, checks for safety rule violations, sends alerts, and offers data analysis through bar graphs, scatter plots, and overtime reports. The project reduces the need for supervision, improves reporting, and allows for quick action when needed. It detects hardhats, safety vests and personnel.

## Key Features Implemented:

- Real-time detection of personnel on construction sites
- Automated tracking of safety equipment (hardh+ats and high-visibility vests)
- Compliance monitoring and reporting system
- Alert system for safety violations
- **Data Analytics:**
    - Bar graphs showing the number and types of entities on site.
    - Scatter-plots showing the working groups and machines at an instant.
- Admin phase-wise analysis for clustering.
- Providing detailed overtime reports showing working hours,worker flow and machinery availability.

## Analysis:

- **Bar Graph:**
The Bar Graph includes the types of Objects detected and number of objects grouped by their class, which helps in identifying all types of machinery and number of workers  currently in the Construction site. Also we can measure the number of people following the safety measure.
- **Scatter-plot:**
Scatter-plot in dashboard has points clustered (connected) based on a threshold distance representing  persons and machinery ,which include current works in the Construction site based on clustering.
- **Zone-Tagger:**
It allows the admin to demarcate zones at the start of each phase of construction such that When the scatter-plot is plotted, we get to know which group of people are working on which area and how many people are working there.
- **Overtime-Reports:**
    
    We can also generate detailed overtime reports that track working hours, worker flow, and machinery availability, helping to optimize workforce and equipment usage. By analyzing this data, it highlights inefficiencies and patterns, enabling better decision-making for staffing, scheduling, and resource allocation, ultimately improving productivity and cost-effectiveness on the construction site.
    

## Technical Achievements

### Detection Accuracy:

| Equipment Type | Detection Accuracy |
| --- | --- |
| Hardhats | 77.4% |
| Safety Vests | 74.2% |
| Personnel Detection | 81.1% |

## Implementation Milestones:

- Initial system deployment and testing
- PPE Dataset collection.
- Annotated images collected from camera.
- Training Model with datasets collected and Annotated images.
- Mobile app development for site supervisors

### Key Benefits Achieved:

- Enhanced workplace safety through proactive monitoring
- Reduced manual supervision requirements
- Improved compliance documentation and reporting
- Real-time intervention capabilities

## Future Enhancements:

- Implementation of predictive analytics for risk assessment
- Progress in Construction site based on image subtraction or semantic segmentations.

## Conclusion:

The Construction Site Monitoring project has successfully demonstrated its effectiveness in improving construction site safety through automated monitoring and real-time intervention capabilities. The system has shown significant impact in reducing workplace incidents and improving safety compliance rates.
