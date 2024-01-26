
![Logo](Miscellaneous/weather-logo.jpeg)



# UEFI Weather APP

This project is part of the Hardware Lab (**CE-40102**) course, featuring a UEFI application designed to display weather information and forecasts for users. The primary focus lies in the ability to interact with a network interface card (**NIC**) within the UEFI environment and initiate a simple **HTTP** request using the tools provided by **EDK II**, the standard UEFI implementation. This project serves as an excellent learning opportunity for working with the fundamentals of the UEFI environment and stands as a valuable reference for those seeking to utilize network interfaces within this setting. The resulting application serves as a convenient tool for users to check the weather upon turning on their computers.


## Tools
Some of the tools and technologies that our project mostly relies on are listed below:
- **Qemu**
- **EDK2**
- **OVMF**
- **KVM**
- `C`
- `Python`


## Implementation Details

Detailed explanations of implementations can be found in this [section](Code/Readme.md).

There is also a comprehensive [report](Document/Readme.md) (in **PDF**) for this project that outlines the steps and challenges encountered.

## How to Run

In this part, you should provide instructions on how to run your project. Also if your project requires any prerequisites, mention them. 

#### Examples:
#### Build Project
Your text comes here
```bash
  build --platform=OvmfPkg/OvmfPkgX64.dsc --arch=X64 --buildtarget=RELEASE --tagname=GCC5
```

#### Run server
Your text comes here
```bash
  pyhton server.py -p 8080
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `-p` | `int` | **Required**. Server port |



## Results
Here, you can observe the results of running our UEFI Weather APP on **Qemu** (version: 4.2.1, 2019). The program is built using **EDK II** (tag version: edk2-stable201911). The following four pictures depict the successful execution of this program in the UEFI shell:

![Successful Execution 1](Miscellaneous/success-exec-1.png)
![Successful Execution 2](Miscellaneous/success-exec-2.png)
![Successful Execution 3](Miscellaneous/success-exec-3.png)
![Successful Execution 4](Miscellaneous/success-exec-4.png)

There are also situations where errors may arise, such as difficulties in finding the network interface or issues in communicating with the API. Our program is designed to handle most known possible errors effectively. The following two pictures illustrate these scenarios and demonstrate how we manage to address them. In the first case, we neglected to execute network configuration commands (as shown in startup.nsh) before running our program, which is necessary to prepare the UEFI shell to communicate with the **NIC**. On the other hand, in the second case, we failed to provide the correct access token for our weather API, resulting in access being denied.

![Failed Execution 1](Miscellaneous/error-exec-1.png)
![Failed Execution 2](Miscellaneous/error-exec-2.png)

## Related Links

 - [**EDK II**](https://github.com/tianocore/edk2)
 - [**Qemu**](https://www.qemu.org/docs/master/)
 - [**Django Doc**](https://docs.djangoproject.com/en/5.0/)


## Authors

- [*Mohammad Sadegh Majidi Yazdi*](https://github.com/sadegh-majidi)
- [*Mahdi Jafari Raviz*](https://github.com/mahdi-jfri)
- [*Solale Mohammadi*](https://github.com/solale427)
