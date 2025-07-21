# 05. Tools and Software Guides

This section of the Fixed-Wing UAV Design Compendium provides an overview and guidance for various software tools critical to the conceptual, preliminary, and detailed design phases of fixed-wing Unmanned Aerial Vehicles (UAVs). Whether for aerodynamic analysis, structural optimization, or multidisciplinary design, these tools facilitate the complex calculations and simulations required in modern aircraft design.

## Related Design Software and Tools

Below is a list of significant software and frameworks commonly used in aerospace design, particularly relevant to UAV development, including their primary applications:

* **[AeroSandbox](https://github.com/peterdsharpe/AeroSandbox)**: A Python library that facilitates rapid aircraft design optimization through automatic differentiation, enabling efficient integration of composable analysis tools for aerodynamics, propulsion, structures, and trajectory design.and optimization tasks.
* **[RCAIDE by LEADs](https://github.com/leadsgroup/RCAIDE_LEADS)**: a framework for performing rapid Overall Aircraft Design. Can be connected with openMDAO
* **[SUAVE](https://github.com/suavecode/SUAVE)**: multi-fidelity conceptual design environment. Its purpose is to credibly produce conceptual-level design conclusions.
* **[FAST (Framework for Aircraft System/Subsystem TRade-offs)](https://github.com/fast-aircraft-design/FAST-OAD)**: An open-source framework dedicated to aircraft conceptual design, enabling trade-off studies across various systems and subsystems.
* **[OpenAeroStruct - MDO Lab](https://github.com/mdolab/OpenAeroStruct/tree/main)**: An aerostructural optimization tool that integrates aerodynamic and structural analysis, forming part of the broader MDO Lab's design tool suite.
* **[Aviumtechnologies APM Docs](https://docs.aviumtechnologies.com)**:  a low-order, unsteady, unstructured potential flow solver for arbitrary geometries suitable for quick what-if design studies.
* **[MACHAERO](https://mdolab-mach-aero.readthedocs-hosted.com/en/latest/)**: An open-source framework for performing gradient-based aerodynamic shape optimization
* **FLIGHTWARE**: A commercial software utilized for flight planning and operational management.
* **[Aviary](https://github.com/OpenMDAO/Aviary/tree/main)**: A specialized library built upon the OpenMDAO framework, designed for advanced aircraft modeling and optimization tasks.
* **[OpenMDAO software suit](https://github.com/OpenMDAO/OpenMDAO)**: A robust Python-based open-source framework that facilitates multidisciplinary design analysis and optimization (MDAO).
* **[CEASIOMpy](https://github.com/cfsengineering/CEASIOMpy/tree/main)**: used to set up complex design and optimisation workflows for both conventional and unconventional aircraft configurations.

## Specific Tool Documentation

This sub-section provides direct access to documentation for key tools included or frequently referenced in this compendium.

### DATCOM

The Digital Combat Aircraft Design (DATCOM) methodology is a widely used reference for aerodynamic data estimation.

* **Primary Manual:**
    * [USAF STABILITY AND CONTROL DATCOM (D. E. HOAK) (Z-Library).pdf](./DATCOM/USAF%20STABILITY%20AND%20CONTROL%20DATCOM%20(D.%20E.%20HOAK)%20(Z-Library).pdf)
* **Datcom Digital Manuals (Specific to the Digital Datcom Implementation):**
    * [DDmanualVol1 - User Manual.pdf](./DATCOM/Datcom%20Digital/DDmanualVol1%20-%20User%20Manual.pdf)
    * [bookmarked_DDmanualVol1 - User Manual.pdf](./DATCOM/Datcom%20Digital/bookmarked_DDmanualVol1%20-%20User%20Manual.pdf) (likely a duplicate or annotated version of Vol1)
    * [DDmanualVol2 - Implementations of Datcom Methods.pdf](./DATCOM/Datcom%20Digital/DDmanualVol2%20-%20Implementations%20of%20Datcom%20Methods.pdf)
    * [DDmanualVol3 - Plot Module.pdf](./DATCOM/Datcom%20Digital/DDmanualVol3%20-%20Plot%20Module.pdf)

### XFLR5

XFLR5 is an analysis tool for airfoils, wings, and planes operating at low Reynolds Numbers. It includes XFoil's direct and inverse analysis capabilities.

* **Key Guidelines:**
    * [Abbreviations.pdf](./XFLR5/Abbreviations.pdf)
    * [XFLR5 Guidelines.pdf](./XFLR5/XFLR5%20Guidelines.pdf)


**Note:** This section will also house user-created tutorials and practical application guides for these and other tools.