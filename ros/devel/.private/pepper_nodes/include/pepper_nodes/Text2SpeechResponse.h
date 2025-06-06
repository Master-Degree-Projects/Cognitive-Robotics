// Generated by gencpp from file pepper_nodes/Text2SpeechResponse.msg
// DO NOT EDIT!


#ifndef PEPPER_NODES_MESSAGE_TEXT2SPEECHRESPONSE_H
#define PEPPER_NODES_MESSAGE_TEXT2SPEECHRESPONSE_H


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
struct Text2SpeechResponse_
{
  typedef Text2SpeechResponse_<ContainerAllocator> Type;

  Text2SpeechResponse_()
    : ack()  {
    }
  Text2SpeechResponse_(const ContainerAllocator& _alloc)
    : ack(_alloc)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> _ack_type;
  _ack_type ack;





  typedef boost::shared_ptr< ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> const> ConstPtr;

}; // struct Text2SpeechResponse_

typedef ::pepper_nodes::Text2SpeechResponse_<std::allocator<void> > Text2SpeechResponse;

typedef boost::shared_ptr< ::pepper_nodes::Text2SpeechResponse > Text2SpeechResponsePtr;
typedef boost::shared_ptr< ::pepper_nodes::Text2SpeechResponse const> Text2SpeechResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator1> & lhs, const ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator2> & rhs)
{
  return lhs.ack == rhs.ack;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator1> & lhs, const ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace pepper_nodes

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "b6a73f722475d64a28238118997ef482";
  }

  static const char* value(const ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xb6a73f722475d64aULL;
  static const uint64_t static_value2 = 0x28238118997ef482ULL;
};

template<class ContainerAllocator>
struct DataType< ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "pepper_nodes/Text2SpeechResponse";
  }

  static const char* value(const ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "string ack\n"
;
  }

  static const char* value(const ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.ack);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Text2SpeechResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::pepper_nodes::Text2SpeechResponse_<ContainerAllocator>& v)
  {
    s << indent << "ack: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>::stream(s, indent + "  ", v.ack);
  }
};

} // namespace message_operations
} // namespace ros

#endif // PEPPER_NODES_MESSAGE_TEXT2SPEECHRESPONSE_H
