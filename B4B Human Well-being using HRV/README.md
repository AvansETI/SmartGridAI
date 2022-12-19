# Project: Brains 4 Buildings Human Well-being using HRV

**The Dutch government aims for a 49% reduction in greenhouse gas emissions in 2030 (compared to 1990).** Even in the most modern buildings, 10-30 % of the energy is lost due to faulty installations or incorrect use of the systems. In addition, the indoor climate is often substandard and the operational costs are high. By giving buildings a ‘brain’, data from smart meters, climate control systems and the Internet of Things (IoT) can be used to make better decisions. Techniques are very promising, but current models and algorithms are not yet fast and efficient enough to actually make buildings smarter, and implementation is difficult.

**To help in this endeavor the brains for buildings (B4B) program was started. B4B aims at leveraging AI and machine learning (ML) models to reduce energy consumption, increase comfort, respond flexibly to user wellbeing and save on installation maintenance costs. ML makes use of the data generated from smart meters, building management systems and IoT devices.**

# Problem statement

**Today existing models (non-ML) are based on averaged responses from a large population and are unable to accommodate the differences in estimating thermal comfort responses of individuals. Besides that, these models have a mismatch with what people actually feel.**

The scope of the project is to explore how AI can be applied to predict in real-time occupant personal comfort based on their feedbacks, metabolic rate (Heart Bit rate Variability and skin temperature) and environmental factors. Personal comfort models can be used to better understand specific comfort needs and desires of individual occupants and characterize a set of conditions that would satisfy their thermal comfort in a given space. Personal comfort models are designed to predict thermal comfort for a single person; hence, they are not necessarily directly applicable to other occupants. However as the amount of data increases, a comfort model will be trained and repeatable patterns may surface that can be generalized to a larger population (gender, age), space types (office, shared space, cubicles, …) or geolocation. Such information can inform the design and control decisions of an energy management system (EMS) to provide optimal satisfaction and energy efficiency.

# Goal

The project is done when a correlation between HRV and personal comfort level is found or when it is sure there is no correlation. If no correlation exists, then we will create a model for personal comfort level with other features. If a correlation exists, a model for predicting comfort level with HRV will be made. This model should be as accurate as reasonably possible within the time limit and with the collected data. After the model is trained and tested, it must be made available for the end users. The occupants and EMS should be able to act on the AI model via a dashboard or another interface.

# Research question

- What is HRV (Heart Rate Variabiltiy)?
- Should HRV be used as an indication for thermal wellbeing.
- How can one measure HRV?
- What metrics are there for HRV?
- How can one retrieve active and passive feedback?
- Does HRV have an impact on a person's well-being?
