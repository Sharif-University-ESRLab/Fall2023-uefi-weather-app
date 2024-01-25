
![Logo](Miscellaneous/weather-logo.jpeg)



# UEFI Weather APP

This project is part of the Hardware Lab (CE-40102) course, featuring a UEFI application designed to display weather information and forecasts for users. The primary focus lies in the ability to interact with a network interface card (NIC) within the UEFI environment and initiate a simple HTTP request using the tools provided by EDK II, the standard UEFI implementation. This project serves as an excellent learning opportunity for working with the fundamentals of the UEFI environment and stands as a valuable reference for those seeking to utilize network interfaces within this setting. The resulting application serves as a convenient tool for users to check the weather upon turning on their computers.


## Tools
Some of the tools and technologies that our project mostly relies on are listed below:
- Qemu
- EDK2
- OVMF
- KVM
- C
- Python


## Implementation Details

In this section, you will explain how you completed your project. It is recommended to use pictures to demonstrate your system model and implementation.


Feel free to use sub-topics for your projects. If your project consists of multiple parts (e.g. server, client, and embedded device), create a separate topic for each one.

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
In this section, you should present your results and provide an explanation for them.

Using image is required.

## Related Links

 - [EDK II](https://github.com/tianocore/edk2)
 - [Qemu](https://www.qemu.org/docs/master/)
 - [Django Doc](https://docs.djangoproject.com/en/5.0/)


## Authors

- [Mohammad Sadegh Majidi Yazdi](https://github.com/sadegh-majidi)
- [Mahdi Jafari Raviz](https://github.com/mahdi-jfri)
- [Solale Mohammadi](https://github.com/solale427)
