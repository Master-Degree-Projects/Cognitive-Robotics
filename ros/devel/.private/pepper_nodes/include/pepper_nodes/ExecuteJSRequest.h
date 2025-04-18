// Generated by gencpp from file pepper_nodes/ExecuteJSRequest.msg
// DO NOT EDIT!


#ifndef PEPPER_NODES_MESSAGE_EXECUTEJSREQUEST_H
#define PEPPER_NODES_MESSAGE_EXECUTEJSREQUEST_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace pepper_nodes
{
template <class ContainerAllocator>
struct ExecuteJSRequest_
{
  typedef ExecuteJSRequest_<ContainerAllocator> Type;

  ExecuteJSRequest_()
    : js()  {
    }
  ExecuteJSRequest_(const ContainerAllocator& _alloc)
    : js(_alloc)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> _js_type;
  _js_type js;





  typedef boost::shared_ptr< ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> const> ConstPtr;

}; // struct ExecuteJSRequest_

typedef ::pepper_nodes::ExecuteJSRequest_<std::allocator<void> > ExecuteJSRequest;

typedef boost::shared_ptr< ::pepper_nodes::ExecuteJSRequest > ExecuteJSRequestPtr;
typedef boost::shared_ptr< ::pepper_nodes::ExecuteJSRequest const> ExecuteJSRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator1> & lhs, const ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator2> & rhs)
{
  return lhs.js == rhs.js;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator1> & lhs, const ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace pepper_nodes

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "e04c1e56762d4f55445fb8ba190fb908";
  }

  static const char* value(const ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xe04c1e56762d4f55ULL;
  static const uint64_t static_value2 = 0x445fb8ba190fb908ULL;
};

template<class ContainerAllocator>
struct DataType< ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "pepper_nodes/ExecuteJSRequest";
  }

  static const char* value(const ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "string js\n"
;
  }

  static const char* value(const ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.js);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct ExecuteJSRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::pepper_nodes::ExecuteJSRequest_<ContainerAllocator>& v)
  {
    s << indent << "js: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>::stream(s, indent + "  ", v.js);
  }
};

} // namespace message_operations
} // namespace ros

#endif // PEPPER_NODES_MESSAGE_EXECUTEJSREQUEST_H
