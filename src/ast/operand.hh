#pragma once

#include <ast/ast.hh>
#include <ast/visitor.hh>
#include <x86/x86.hh>

#include <string>
#include <memory>

namespace nolimix86
{

  namespace ast
  {

    class operand : public ast
    {
      /// Operand tags
      public:
        struct temp_tag {};
        struct reg_tag {};
        struct imm_tag {};
        struct mem_tag {};

      public:
        /// Create an operand represented by a temporary.
        operand(size_t, temp_tag);

        /// Create an operand represented by a machine register.
        operand(const std::string&);

        /// Create an operand represented by an immediate.
        operand(size_t);

        /// Create an operand represented by a memory access.
        /// Arguments: offset, register.
        operand(size_t, const std::string&);

        void accept(const_visitor&) const override;
        void accept(visitor&) override;

      private:
        struct impl
        {
        };

        /// Implementation of the operand as a temporary.
        struct temp_impl : public impl
        {
          /// The number of the temporary.
          size_t temp_num_ = 0;

          temp_impl(size_t);
        };

        /// Implementation of the operand as a register.
        struct reg_impl : public impl
        {
          /// The register.
          enum x86::reg reg_ = x86::UNKNOWN;

          reg_impl(const std::string&);
        };

        /// Implementation of the operand as a immediate.
        struct imm_impl : public impl
        {
          /// The value of the immediate.
          size_t value_ = 0;

          imm_impl(size_t);
        };

        /// Implementation of the operand as a memory access.
        struct mem_impl : public impl
        {
          /// The value of the offset.
          size_t offset_ = 0;

          /// The register.
          enum x86::reg reg_ = x86::UNKNOWN;

          mem_impl(size_t, const std::string&);
        };

        /// The imlementation detail.
        std::unique_ptr<impl> impl_;
    };

  } // namespace ast

} // namespace nolimix86